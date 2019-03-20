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
        parse = reqparse.RequestParser()
        parse.add_argument('namaProduk', location='args', required=True)
        parse.add_argument('harga', location='args',  required=True)
        parse.add_argument('kategori', location='args',  required=True)
        parse.add_argument('foto_produk', location='args',  required=True)
        parse.add_argument('deskripsi_produk', location='args',  required=True)

        args = parse.parse_args()

        produk_baru = Produk(None, penjual['id'], penjual['username'], args['namaProduk'], args['harga'], args['kategori'], args['foto_produk'], args['deskripsi_produk'])
        db.session.add(produk_baru)
        db.session.commit()

        # return 
        return {"message": "INPUT PRODUCT SUCCESS", 'product': marshal(produk_baru, Produk.response_field)}, 200, {'Content-Type': 'application/jason'}
    
    ##### Melihat Produk dan Produk detail dari Penjual
    @jwt_required
    def get(self, idProduk=None):
        penjual = get_jwt_claims()
        
        if idProduk == None:
            qry = Produk.query.filter_by(penjual_id=penjual['id']).all()

            rows = []
            for row in qry:
                temp = marshal(row, Produk.response_field)
                rows.append(temp)
            
            return rows, 200, {'Content-Type': 'application/jason'}
        
        else:
            qry = Produk.query.filter_by(penjual_id=penjual['id']).filter_by(id=idProduk).first()
            if qry is not None:
                return marshal(qry, Produk.response_field), 200, {'Content-Type': 'application/jason'}
            else:
                return {'status': 'NOT_FOUND'}, 404, {'Content-Type': 'application/json'}


    ##### EDIT PRODUK oleh PENJUAL
    @jwt_required
    def put(self, idProduk):
        penjual = get_jwt_claims()
        
        qry_produk = Produk.query.filter_by(penjual_id=penjual['id']).filter_by(id=idProduk).first()

        if qry_produk is None:
            return {'status': 'NOT_FOUND'}, 404, {'Content-Type': 'application/json'}

        else:
            produk = marshal(qry_produk, Produk.response_field)

            parse = reqparse.RequestParser()
            parse.add_argument('namaProduk', location='args', default = produk['namaProduk'])
            parse.add_argument('harga', location='args',  default = produk['harga'])
            parse.add_argument('kategori', location='args',  default = produk['kategori'])
            parse.add_argument('foto_produk', location='args',  default = produk['foto_produk'])
            parse.add_argument('deskripsi_produk', location='args',  default = produk['deskripsi_produk'])

            args = parse.parse_args()

            qry_produk.namaProduk = args['namaProduk']
            qry_produk.harga = args['harga']
            qry_produk.kategori = args['kategori']
            qry_produk.foto_produk = args['foto_produk']
            qry_produk.deskripsi_produk = args['deskripsi_produk']

            db.session.commit()
            return marshal(qry_produk, Produk.response_field), 200, {'Content-Type': 'application/json'}
    
    ##### HAPUS PRODUK oleh Penjual
    @jwt_required
    def delete(self, idProduk):
        penjual = get_jwt_claims()

        qry_produk = Produk.query.filter_by(penjual_id = penjual['id']).filter_by(id = idProduk).first()

        if qry_produk is not None:
            db.session.delete(qry_produk)
            db.session.commit()
            return {'status': 'DATA_DELETED'}, 200, {'Content-Type': 'application/json'}
        else:
            return {'status': 'NOT_FOUND'}, 404, {'Content-Type': 'application/json'}

##### Endpoint Produk-Penjual
api.add_resource(ProdukPenjual, '/penjual/produk', '/penjual/produk/<int:idProduk>')


############################# Public melihat Produk #############################
class Public(Resource):
    
    def get(self, idProduk = None):

        if idProduk == None:
            parse = reqparse.RequestParser()
            parse.add_argument('p', type=int, location='args', default=1)
            parse.add_argument('rp', type=int, location='args', default=9)
            parse.add_argument('search', location='args')
            args = parse.parse_args()

            offset = (args['p'] * args['rp']) - args['rp']

            qry_produk = Produk.query
            if args['search'] is not None:
                qry_produk = qry_produk.filter(Produk.penjual.like("%"+args['search']+"%"))
                if qry_produk.first() is None:
                    qry_produk = Produk.query.filter(Produk.namaProduk.like("%"+args['search']+"%"))
                    if qry_produk.first() is None:
                        qry_produk = Produk.query.filter(Produk.kategori.like("%"+args['search']+"%"))
                        if qry_produk.first() is None:
                            qry_produk = Produk.query.filter(Produk.deskripsi_produk.like("%"+args['search']+"%"))
                            if qry_produk.first() is None:
                                return {'status': 'NOT_FOUND','message':'item not found'},404, { 'Content-Type': 'application/json' }
            
            rows = [{'halaman': args['p']}]
            for row in qry_produk.limit(args['rp']).offset(offset).all():
                rows.append(marshal(row, Produk.response_field))
            return rows, 200, {'Content-Type': 'application/json'}

        else:
            qry_produk = Produk.query.get(idProduk)
            if qry_produk is not None:
                return marshal(qry_produk, Produk.response_public), 200, {'Content-Type': 'application/json'}
            else:
                return {'status': 'NOT_FOUND'}, 404, {'Content-Type': 'application/json'}

##### Endpoint Public
api.add_resource(Public, '/public', '/public/<int:idProduk>')       