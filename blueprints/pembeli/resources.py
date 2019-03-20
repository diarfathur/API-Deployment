import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from . import *
from blueprints import db
from blueprints.pembeli import Pembeli
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_pembeli = Blueprint('Pembeli', __name__)
api = Api(bp_pembeli)


class PembeliResource(Resource):
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('username', location='args', required=True)
        parse.add_argument('password', location='args', required=True)
        parse.add_argument('contact', location='args',  required=True)
        parse.add_argument('status', location='args', default='pembeli')
        parse.add_argument('email', location='args', required=True)
        parse.add_argument('address', location='args', required=True)

        args = parse.parse_args()

        pembeliBaru = Pembeli(None, args['username'], args['password'], args['contact'], args['status'], args['email'], args['address'])
        db.session.add(pembeliBaru)
        db.session.commit()        

        return marshal(pembeliBaru, Pembeli.response_field), 200, {'Content-Type': 'application/json'}

    @jwt_required
    def get(self):
        pembeli = get_jwt_claims()

        qry = Pembeli.query.get(pembeli['id'])
        result = marshal(qry, Pembeli.response_pembeli)
        return result, 200, {'Content-Type': 'application/json'}
            
    @jwt_required
    def put(self):#, usernamePenbeli):
        pembeli = get_jwt_claims()

        qry = Pembeli.query.get(pembeli['id'])  
        data_pembeli = marshal(qry, Pembeli.response_field)

        # if usernamePembeli != pembeli['username']:
        #     return {'message': "ACCESS_DENIED"}, 404, {'Content-Type': 'application/json'}

        # else:
        parse =reqparse.RequestParser()
        parse.add_argument('username', location='json', default = data_pembeli['username'])
        parse.add_argument('password', location='json', default = data_pembeli['password'])
        parse.add_argument('contact', location='json', default = data_pembeli['email'])
        parse.add_argument('email', location='json', default = data_pembeli['email'])
        parse.add_argument('address', location='json', default = data_pembeli['address'])

        args = parse.parse_args()

        qry.username = args['username']
        qry.password = args['password']
        qry.contact = args['contact']
        qry.email = args['email']
        qry.address = args['address']
        db.session.commit()

        return {'message': 'DATA_UPDATED', 'input': marshal(qry, Pembeli.response_field)}, 200, {'Content-Type': 'application/json'}

    @jwt_required
    def delete(self):#, usernamePenbeli):
        pembeli = get_jwt_claims()
        qry = Pembeli.query.get(pembeli['id'])

        db.session.delete(qry)
        db.session.commit()
        return {'message': 'DATA_DELETED'}, 200, {'Content-Type': 'application/json'}


api.add_resource(PembeliResource, '/pembeli/profile')
        