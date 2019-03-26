import json, logging, hashlib
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from . import *
from blueprints import db
from blueprints.penjual import Penjual
from blueprints.pembeli import Pembeli
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

bp_login = Blueprint('login', __name__)
api = Api(bp_login)

class LoginPenjual(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location = 'json', required = True)
        parser.add_argument('password', location = 'json', required = True)
        args = parser.parse_args()

        password = hashlib.md5(args['password'].encode()).hexdigest()

        qry = Penjual.query.filter_by(username = args['username']).filter_by(password = password).first()


        if qry is not None:
            token = create_access_token(identity = marshal(qry, Penjual.response_token))
            statusUser = qry.status
        else:
            return {'status': 'UNAUTORIZED', 'message': 'Invalid username or password'}, 401
        return {'status': 'Success', 'message': 'You got authorization for your account', 'statusUser': statusUser, 'token' : token}, 200, {'Content-Type': 'application/json'}

api.add_resource(LoginPenjual, '/login/penjual')


class LoginPembeli(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location = 'json', required = True)
        parser.add_argument('password', location = 'json', required = True)
        args = parser.parse_args()

        password = hashlib.md5(args['password'].encode()).hexdigest()
        qry = Pembeli.query.filter_by(username = args['username']).filter_by(password = password).first()


        if qry is not None:
            token = create_access_token(identity = marshal(qry, Pembeli.response_token))
            statusUser = qry.status
        else:
            return {'status': 'UNAUTORIZED', 'message': 'Invalid username or password'}, 401
        return {'status': 'Success', 'message': 'You got authorization for your account', 'statusUser': statusUser, 'token' : token}, 200, {'Content-Type': 'application/json'}

api.add_resource(LoginPembeli, '/login/pembeli')
