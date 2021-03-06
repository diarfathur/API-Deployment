import json, logging, hashlib
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
        parse.add_argument('username', location='json', required=True)
        parse.add_argument('password', location='json', required=True)
        parse.add_argument('fullName', location='json', required=True)
        parse.add_argument('contact', location='json',  required=True)
        parse.add_argument('email', location='json', required=True)
        parse.add_argument('address', location='json', required=True)
        parse.add_argument('fullName', location='json', required=True)

        args = parse.parse_args()

        qry = Pembeli.query.filter_by(username = args['username']).first()
        if qry is not None:
            return {'status':'Not Acceptable', 'message': 'USERNAME_ALREADY_IN_USE'}, 406, {'Content-Type': 'application/json'}

        password = hashlib.md5(args['password'].encode()).hexdigest()

        pembeliBaru = Pembeli(None, args['username'], password, args['fullName'], args['contact'], 'pembeli', args['email'], args['address'])
        db.session.add(pembeliBaru)
        db.session.commit()

        pembeliBaru = marshal(pembeliBaru, Pembeli.response_pembeli)    

        return {"status": "Created", "message": "Your account has been created", "input": pembeliBaru}, 201, {'Content-Type': 'application/json'}

    @jwt_required
    def get(self):
        pembeli = get_jwt_claims()
        if pembeli['status'] != 'pembeli':
            return {"status": "Unauthorized", "message": "Access Denied"}, 401, {'Content-Type': 'application/json'}
        
        qry = Pembeli.query.get(pembeli['id'])
        if qry == None:
            return {'status':'Not Found', 'message': 'DATA_NOT_FOUND'}, 404, {'Content-Type': 'application/json'}
        
        result = marshal(qry, Pembeli.response_pembeli)
        return {"status":"OK", "message":"Get Buyer Account", "buyer": result}, 200, {'Content-Type': 'application/json'}
            
    @jwt_required
    def put(self):
        pembeli = get_jwt_claims()
        if pembeli['status'] != 'pembeli':
            return {"status": "Unauthorized", "message": "Access Denied"}, 401, {'Content-Type': 'application/json'}

        qry = Pembeli.query.get(pembeli['id'])

        if qry == None:
            return {'status':'Not Found', 'message': 'DATA_NOT_FOUND'}, 404, {'Content-Type': 'application/json'}

        data_pembeli = marshal(qry, Pembeli.response_field)

        parse =reqparse.RequestParser()
        parse.add_argument('username', location='json', default = data_pembeli['username'])
        parse.add_argument('password', location='json', default = data_pembeli['password'])
        parse.add_argument('fullName', location='json', default = data_pembeli['fullName'])
        parse.add_argument('contact', location='json', default = data_pembeli['contact'])
        parse.add_argument('email', location='json', default = data_pembeli['email'])
        parse.add_argument('address', location='json', default = data_pembeli['address'])

        args = parse.parse_args()

        password = hashlib.md5(args['password'].encode()).hexdigest()

        qry.username = args['username']
        qry.password = password
        qry.fullName = args['fullName']
        qry.contact = args['contact']
        qry.email = args['email']
        qry.address = args['address']
        db.session.commit()

        return {'status':'Accepted', 'message': 'DATA_UPDATED', 'updated_data': marshal(qry, Pembeli.response_pembeli)}, 202, {'Content-Type': 'application/json'}

    @jwt_required
    def delete(self):
        pembeli = get_jwt_claims()
        if pembeli['status'] != 'pembeli':
            return {"status": "Unauthorized", "message": "Access Denied"}, 401, {'Content-Type': 'application/json'}

        qry = Pembeli.query.get(pembeli['id'])
        if qry == None:
            return {'status':'Not Found', 'message': 'DATA_NOT_FOUND'}, 404, {'Content-Type': 'application/json'}

        data_pembeli = marshal(qry, Pembeli.response_pembeli)

        db.session.delete(qry)
        db.session.commit()
        return {'status':'OK', 'message': 'DATA_DELETED', 'buyer': data_pembeli}, 200, {'Content-Type': 'application/json'}


api.add_resource(PembeliResource, '/pembeli')
        