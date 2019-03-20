import json, logging, hashlib
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from . import *
from blueprints import db
from blueprints.penjual import Penjual
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_penjual = Blueprint('Penjual', __name__)
api = Api(bp_penjual)


class PenjualResource(Resource):

    # Buat Akun Penjual Baru
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('username', location='args', required=True)
        parse.add_argument('password', location='args',  required=True)
        parse.add_argument('contact', type=int, location='args', required=True)
        parse.add_argument('email', location='args', required=True)
        parse.add_argument('address', location='args', required=True)
        parse.add_argument('foto_profil', location='args')
        parse.add_argument('deskripsi_penjual', location='args')

        args = parse.parse_args()

        qry = Penjual.query.filter_by(username = args['username']).first()
        if qry is not None:
            return {'status':'Not Acceptable', 'message': 'USERNAME_ALREADY_IN_USE'}, 406, {'Content-Type': 'application/json'}
        
        password = hashlib.md5(args['password'].encode()).hexdigest()

        penjualBaru = Penjual(None, args['username'], password, args['contact'], 'penjual', args['email'], args['address'], args['foto_profil'], args['deskripsi_penjual'])
        db.session.add(penjualBaru)
        db.session.commit()

        penjualBaru = marshal(penjualBaru, Penjual.response_penjual)

        return {"status": "Created", "message": "Your account has been created", "input": penjualBaru}, 201, {'Content-Type': 'application/json'}

    # Penjual melihat profilnya sendiri
    @jwt_required
    def get(self):
        penjual = get_jwt_claims()
        
        qry = Penjual.query.get(penjual['id'])
        if qry == None:
            return {'status':'Not Found', 'message': 'DATA_NOT_FOUND'}, 404, {'Content-Type': 'application/json'}

        result = marshal(qry, Penjual.response_penjual)
        return {"status":"OK", "message":"Get Seller Account", "seller": result}, 200, {'Content-Type': 'application/json'}

    # Penjual Mengubah Akunnya Sendiri
    @jwt_required
    def put(self):
        penjual = get_jwt_claims()
        
        qry = Penjual.query.get(penjual['id'])
        
        if qry == None:
            return {'status':'Not Found', 'message': 'DATA_NOT_FOUND'}, 404, {'Content-Type': 'application/json'}
        
        data_penjual = marshal(qry, Penjual.response_field)

        parse =reqparse.RequestParser()
        parse.add_argument('username', location='args', default = data_penjual['username'])
        parse.add_argument('password', location='args', default = data_penjual['password'])
        parse.add_argument('contact', location='args', default = data_penjual['contact'])
        parse.add_argument('email', location='args', default = data_penjual['email'])
        parse.add_argument('address', location='args', default = data_penjual['address'])
        parse.add_argument('foto_profil', location='args', default = data_penjual['foto_profil'])
        parse.add_argument('deskripsi_penjual', location='args', default = data_penjual['deskripsi_penjual'])

        args = parse.parse_args()

        qry.username = args['username']
        qry.password = args['password']
        qry.contact = args['contact']
        qry.email = args['email']
        qry.address = args['address']
        qry.foto_profil = args['foto_profil']
        qry.deskripsi_penjual = args['deskripsi_penjual']
        db.session.commit()

        return {'status':'Accepted', 'message': 'DATA_UPDATED', 'seller': marshal(qry, Penjual.response_penjual)}, 202, {'Content-Type': 'application/json'}

    # Peenjual Menghapus Akunnya Sendiri
    @jwt_required
    def delete(self):
        penjual = get_jwt_claims()
        qry = Penjual.query.get(penjual['id'])

        if qry == None:
            return {'status':'Not Found', 'message': 'DATA_NOT_FOUND'}, 404, {'Content-Type': 'application/json'}

        data_penjual = marshal(qry, Penjual.response_penjual)

        db.session.delete(qry)
        db.session.commit()
        return {'status':'OK', 'message': 'DATA_DELETED', 'seller': data_penjual}, 200, {'Content-Type': 'application/json'}


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
