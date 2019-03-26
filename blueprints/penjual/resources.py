import json, logging, hashlib
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from . import *
from blueprints import db
from blueprints.penjual import Penjual
from blueprints.produk import Produk
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_penjual = Blueprint('Penjual', __name__)
api = Api(bp_penjual)


class PenjualResource(Resource):

    # Buat Akun Penjual Baru
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('username', location='json', required=True)
        parse.add_argument('password', location='json',  required=True)
        parse.add_argument('shopName', location='json', required=True)
        parse.add_argument('contact', location='json', required=True)
        parse.add_argument('email', location='json', required=True)
        parse.add_argument('address', location='json', required=True)
        parse.add_argument('foto_profil', location='json')
        parse.add_argument('deskripsi_penjual', location='json')

        args = parse.parse_args()

        qry = Penjual.query.filter_by(username = args['username']).first()
        if qry is not None:
            return {'status':'Not Acceptable', 'message': 'USERNAME_ALREADY_IN_USE'}, 406, {'Content-Type': 'application/json'}
        
        password = hashlib.md5(args['password'].encode()).hexdigest()

        penjualBaru = Penjual(None, args['username'], password, args['shopName'], args['contact'], 'penjual', args['email'], args['address'], args['foto_profil'], args['deskripsi_penjual'])
        db.session.add(penjualBaru)
        db.session.commit()

        penjualBaru = marshal(penjualBaru, Penjual.response_penjual)

        return {"status": "Created", "message": "Your account has been created", "input": penjualBaru}, 201, {'Content-Type': 'application/json'}

    # Penjual melihat profilnya sendiri
    @jwt_required
    def get(self):
        penjual = get_jwt_claims()
        if penjual['status'] != 'penjual':
            return {"status": "Unauthorized", "message": "Access Denied"}, 401, {'Content-Type': 'application/json'}

        qry = Penjual.query.get(penjual['id'])
        if qry == None:
            return {'status':'Not Found', 'message': 'DATA_NOT_FOUND'}, 404, {'Content-Type': 'application/json'}

        result = marshal(qry, Penjual.response_penjual)
        return {"status":"OK", "message":"Get Seller Account", "seller": result}, 200, {'Content-Type': 'application/json'}

    # Penjual Mengubah Akunnya Sendiri
    @jwt_required
    def put(self):
        penjual = get_jwt_claims()
        if penjual['status'] != 'penjual':
            return {"status": "Unauthorized", "message": "Access Denied"}, 401, {'Content-Type': 'application/json'}

        qry = Penjual.query.get(penjual['id'])
        data_penjual = marshal(qry, Penjual.response_field)
        qry_produk = Produk.query.filter_by(penjual_id=penjual['id']).all()

        if qry == None:
            return {'status':'Not Found', 'message': 'DATA_NOT_FOUND'}, 404, {'Content-Type': 'application/json'}

        parse =reqparse.RequestParser()
        parse.add_argument('username', location='json', default = data_penjual['username'])
        parse.add_argument('password', location='json', default = data_penjual['password'])
        parse.add_argument('shopName', location='json', default = data_penjual['shopName'])
        parse.add_argument('contact', location='json', default = data_penjual['contact'])
        parse.add_argument('email', location='json', default = data_penjual['email'])
        parse.add_argument('address', location='json', default = data_penjual['address'])
        parse.add_argument('foto_profil', location='json', default = data_penjual['foto_profil'])
        parse.add_argument('deskripsi_penjual', location='json', default = data_penjual['deskripsi_penjual'])

        args = parse.parse_args()

        password = hashlib.md5(args['password'].encode()).hexdigest()

        for each in qry_produk:
            each.penjual = args['shopName']

        qry.username = args['username']
        qry.password = password
        qry.shopName = args['shopName']
        qry.contact = args['contact']
        qry.email = args['email']
        qry.address = args['address']
        qry.foto_profil = args['foto_profil']
        qry.deskripsi_penjual = args['deskripsi_penjual']
        db.session.commit()

        after = marshal(qry, Penjual.response_penjual)

        return {'status':'Accepted', 'message': 'DATA_UPDATED', 'updated_data': after}, 202, {'Content-Type': 'application/json'}

    # Peenjual Menghapus Akunnya Sendiri
    @jwt_required
    def delete(self):
        penjual = get_jwt_claims()
        if penjual['status'] != 'penjual':
            return {"status": "Unauthorized", "message": "Access Denied"}, 401, {'Content-Type': 'application/json'}
       
        qry = Penjual.query.get(penjual['id'])
        qry_produk = Produk.query.filter_by(penjual_id=penjual['id']).all()

        if qry == None:
            return {'status':'Not Found', 'message': 'DATA_NOT_FOUND'}, 404, {'Content-Type': 'application/json'}

        data_penjual = marshal(qry, Penjual.response_penjual)
        
        produkList = []
        for produk in qry_produk:
            temp = marshal(produk, Produk.response_public)
            produkList.append(temp)
            db.session.delete(produk)

        db.session.delete(qry)
        db.session.commit()
        return {'status':'OK', 'message': 'DATA_DELETED', 'seller': data_penjual, 'products': produkList}, 200, {'Content-Type': 'application/json'}


api.add_resource(PenjualResource, '/penjual')

######################## PUBLIC MELIHAT PROFIL PENJUAL ########################
class PublicPenjual(Resource):
    
    def get(self, idPenjual=None):
        if idPenjual == None:
            parse = reqparse.RequestParser()
            parse.add_argument('p', type=int, location='args', default=1)
            parse.add_argument('rp', type=int, location='args', default=10)
            args = parse.parse_args()

            offset = (args['p'] * args['rp']) - args['rp']

            qry_penjual = Penjual.query
           
            rows = []
            for row in qry_penjual.limit(args['rp']).offset(offset).all():
                rows.append(marshal(row, Penjual.response_penjual))
            return {'status':'OK', 'message':'Get all sellers', 'page': args['p'], 'sellers': rows}, 200, {'Content-Type': 'application/json'}
        
        else:
            qry_penjual = Penjual.query.filter_by(id = idPenjual).first()
            if qry_penjual is not None:
                return {'status':'OK', 'message':'Get a seller', 'seller': marshal(qry, Penjual.response_penjual)}, 200, {'Content-Type': 'application/jason'}

            else:
                return {'status':'Not Found!', 'message': 'DATA_NOT_FOUND'}, 404, {'Content-Type': 'application/json'}

api.add_resource(PublicPenjual, '/public/penjual', '/public/penjual/<int:idPenjual>')#, '/penjual/<str:usernamePenjual>')
