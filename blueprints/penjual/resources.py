import json, logging
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
        parse.add_argument('status', type=int, location='args', default='penjual')        
        parse.add_argument('email', location='args', required=True)
        parse.add_argument('address', location='args', required=True)
        parse.add_argument('foto_profil', location='args')
        parse.add_argument('deskripsi_penjual', location='args')

        args = parse.parse_args()

        qry = Penjual.query.filter_by(username = args['username']).first()
        if qry is not None:
            return {'message': 'USERNAME_ALREADY_IN_USE'}

        penjual_baru = Penjual(None, args['username'], args['password'], args['contact'], args['status'], args['email'], args['address'], args['foto_profil'], args['deskripsi_penjual'])
        db.session.add(penjual_baru)
        db.session.commit()

        return {"message": "SUCCESS"}, 200, {'Content-Type': 'application/json'}

    # Penjual melihat profilnya sendiri
    @jwt_required
    def get(self):#, usernamePenjual):
        penjual = get_jwt_claims()
        
        # if usernamePenjual != penjual['username']:
        #     return {'message': "ACCESS_DENIED"}, 404, {'Content-Type': 'application/json'}

        # else:
        qry = Penjual.query.get(penjual['id'])
        result = marshal(qry, Penjual.response_penjual)
        return result, 200, {'Content-Type': 'application/json'}

    # Penjual Mengubah Akunnya Sendiri
    @jwt_required
    def put(self):#, usernamePenjual):
        penjual = get_jwt_claims()
        
        qry = Penjual.query.get(penjual['id'])
        data_penjual = marshal(qry, Penjual.response_field)

        # if usernamePenjual != penjual['username']:
        #     return {'message': "ACCESS_DENIED"}, 404, {'Content-Type': 'application/json'}

        # else:
        parse =reqparse.RequestParser()
        parse.add_argument('username', location='json', default = data_penjual['username'])
        parse.add_argument('password', location='json', default = data_penjual['password'])
        parse.add_argument('contact', location='json', default = data_penjual['contact'])
        parse.add_argument('email', location='json', default = data_penjual['email'])
        parse.add_argument('address', location='json', default = data_penjual['address'])
        parse.add_argument('foto_profil', location='json', default = data_penjual['foto_profil'])
        parse.add_argument('deskripsi_penjual', location='json', default = data_penjual['deskripsi_penjual'])

        args = parse.parse_args()

        qry.username = args['username']
        qry.password = args['password']
        qry.contact = args['contact']
        qry.email = args['email']
        qry.address = args['address']
        qry.foto_profil = args['foto_profil']
        qry.deskripsi_penjual = args['deskripsi_penjual']
        db.session.commit()

        return {'message': 'DATA_UPDATED', 'input': marshal(qry, Penjual.response_field)}, 200, {'Content-Type': 'application/json'}

    # Peenjual Menghapus Akunnya Sendiri
    @jwt_required
    def delete(self):#, usernamePenjual):
        penjual = get_jwt_claims()
        qry = Penjual.query.get(penjual['id'])

        db.session.delete(qry)
        db.session.commit()
        return {'message': 'DATA_DELETED'}, 200, {'Content-Type': 'application/json'}


api.add_resource(PenjualResource, '/penjual/profile')#, '/penjual/<str:usernamePenjual>')


######################## PUBLIC MELIHAT PROFIL PENJUAL ########################
class PublicPenjual(Resource):
    
    def get(self, usernamePenjual=None):
        if usernamePenjual == None:
            parse = reqparse.RequestParser()
            parse.add_argument('p', type=int, location='args', default=1)
            parse.add_argument('rp', type=int, location='args', default=10)
            parse.add_argument('penjual', location='args')
            args = parse.parse_args()

            offset = (args['p'] * args['rp']) - args['rp']

            qry_penjual = Penjual.query
            if args['penjual'] is not None:
                qry_penjual = qry_penjual.filter(Penjual.username.like("%"+args['penjual']+"%"))
                if qry_penjual.first() is None:
                    return {'status': 'NOT_FOUND','message':'item not found'},404, { 'Content-Type': 'application/json' }


            rows = [{'halaman': args['p']}]
            for row in qry_penjual.limit(args['rp']).offset(offset).all():
                rows.append(marshal(row, Penjual.response_penjual))
            return rows, 200, {'Content-Type': 'application/json'}
        
        else:
            qry_penjual = Penjual.query.filter_by(username = usernamePenjual).first()
            if qry_penjual is not None:
                return marshal(qry_penjual, Penjual.response_penjual), 200, {'Content-Type': 'application/json'}
            else:
                return {'status': 'NOT_FOUND'}, 404, {'Content-Type': 'application/json'}

api.add_resource(PublicPenjual, '/public/penjual', '/public/penjual/<usernamePenjual>')#, '/penjual/<str:usernamePenjual>')
