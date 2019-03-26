import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from . import *
from blueprints import db
from blueprints.penjual import Penjual
from blueprints.produk import Produk
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_produk = Blueprint('Produk', __name__) # url_prefix = '/buku'
api = Api(bp_produk)


class ProdukPenjual(Resource):

    ##### Produk Baru dari Penjual
    @jwt_required
    def post(self):
        penjual = get_jwt_claims()

        if penjual['status'] != 'penjual':
            return {"status": "Unauthorized", "message": "Access Denied"}, 401, {'Content-Type': 'application/json'}
            

        parse = reqparse.RequestParser()
        parse.add_argument('namaProduk', location='json', required=True)
        parse.add_argument('qty', location='json', type=int, required=True)
        parse.add_argument('harga', location='json', type=int, required=True)
        parse.add_argument('kategori', location='json',  required=True)
        parse.add_argument('foto_produk', location='json',  required=True)
        parse.add_argument('deskripsi_produk', location='json',  required=True)

        args = parse.parse_args()

        produk_baru = Produk(None, penjual['id'], penjual['shopName'], args['namaProduk'], args['qty'], args['harga'], args['kategori'], args['foto_produk'], args['deskripsi_produk'])
        db.session.add(produk_baru)
        db.session.commit()

        return {"status": "Created", "message": "Input New Product Success", "product": marshal(produk_baru, Produk.response_field)}, 201, {'Content-Type': 'application/json'}
    
    ##### Melihat Produk dan Produk detail dari Penjual
    @jwt_required
    def get(self, idProduk=None):
        penjual = get_jwt_claims()
        
        if penjual['status'] != 'penjual':
            return {"status": "Unauthorized", "message": "Access Denied"}, 401, {'Content-Type': 'application/json'}

        if idProduk == None:
            qry = Produk.query.filter_by(penjual_id=penjual['id']).all()

            rows = []
            for row in qry:
                temp = marshal(row, Produk.response_field)
                rows.append(temp)
            
            return {'status':'OK', 'message':'Get all products', 'products': rows}, 200, {'Content-Type': 'application/jason'}
        
        else:
            qry = Produk.query.filter_by(penjual_id=penjual['id']).filter_by(id=idProduk).first()
            if qry is not None:
                return {'status':'OK', 'message':'Get a product', 'productDetail': marshal(qry, Produk.response_field)}, 200, {'Content-Type': 'application/jason'}
            else:
                return {'status':'Not Found!', 'message': 'DATA_NOT_FOUND'}, 404, {'Content-Type': 'application/json'}


    ##### EDIT PRODUK oleh PENJUAL
    @jwt_required
    def put(self, idProduk):
        penjual = get_jwt_claims()

        if penjual['status'] != 'penjual':
            return {"status": "Unauthorized", "message": "Access Denied"}, 401, {'Content-Type': 'application/json'}
        
        qry_produk = Produk.query.filter_by(penjual_id=penjual['id']).filter_by(id=idProduk).first()

        if qry_produk is None:
            return {'status':'Not Found!', 'message': 'DATA_NOT_FOUND'}, 404, {'Content-Type': 'application/json'}

        else:
            produk = marshal(qry_produk, Produk.response_field)

            parse = reqparse.RequestParser()
            parse.add_argument('namaProduk', location='json', default = produk['namaProduk'])
            parse.add_argument('qty', location='json', type=int, default = produk['qty'])
            parse.add_argument('harga', location='json', type=int, default = produk['harga'])
            parse.add_argument('kategori', location='json',  default = produk['kategori'])
            parse.add_argument('foto_produk', location='json',  default = produk['foto_produk'])
            parse.add_argument('deskripsi_produk', location='json',  default = produk['deskripsi_produk'])

            args = parse.parse_args()

            qry_produk.namaProduk = args['namaProduk']
            qry_produk.qty = args['qty']
            qry_produk.harga = args['harga']
            qry_produk.kategori = args['kategori']
            qry_produk.foto_produk = args['foto_produk']
            qry_produk.deskripsi_produk = args['deskripsi_produk']

            db.session.commit()
            return {'status':'Accepted', 'message': 'DATA_UPDATED', 'product': marshal(qry_produk, Produk.response_public)}, 202, {'Content-Type': 'application/json'}
    
    ##### HAPUS PRODUK oleh Penjual
    @jwt_required
    def delete(self, idProduk):
        penjual = get_jwt_claims()

        if penjual['status'] != 'penjual':
            return {"status": "Unauthorized", "message": "Access Denied"}, 401, {'Content-Type': 'application/json'}

        qry_produk = Produk.query.filter_by(penjual_id = penjual['id']).filter_by(id = idProduk).first()

        if qry_produk is not None:
            product = marshal(qry_produk, Produk.response_public)
            db.session.delete(qry_produk)
            db.session.commit()
            return {'status':'OK', 'message': 'DATA_DELETED', 'product': product}, 200, {'Content-Type': 'application/json'}
       
        else:
            return {'status':'Not Found!', 'message': 'DATA_NOT_FOUND'}, 404, {'Content-Type': 'application/json'}

##### Endpoint Produk-Penjual
api.add_resource(ProdukPenjual, '/penjual/produk', '/penjual/produk/<int:idProduk>')


############################# Public melihat Produk #############################
class Public(Resource):
    
    def get(self, idProduk = None):

        if idProduk == None:
            parse = reqparse.RequestParser()
            parse.add_argument('p', type=int, location='args', default=1)
            parse.add_argument('rp', type=int, location='args', default=12)
            args = parse.parse_args()

            offset = (args['p'] * args['rp']) - args['rp']

            qry_produk = Produk.query
            
            rows = []
            for row in qry_produk.limit(args['rp']).offset(offset).all():
                rows.append(marshal(row, Produk.response_field))
            return {'status':'OK', 'message': 'All products', 'halaman': args['p'], 'products': rows}, 200, {'Content-Type': 'application/json'}
        else:
            qry_produk = Produk.query.get(idProduk)
            
            if qry_produk is not None:
                return {'status':'OK', 'message':'Get a product', 'product': marshal(qry_produk, Produk.response_public)}, 200, {'Content-Type': 'application/jason'}

            else:
                return {'status':'Not Found!', 'message': 'Product Not Found!'}, 404, {'Content-Type': 'application/json'}

##### Endpoint Public
api.add_resource(Public, '/public', '/public/<int:idProduk>')       