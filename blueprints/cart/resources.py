import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from . import *
from blueprints import db
from blueprints.pembeli import Pembeli
from blueprints.produk import Produk
from blueprints.cart import Cart
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_cart = Blueprint('Cart', __name__) # url_prefix = '/buku'
api = Api(bp_cart)


class CartPembeli(Resource):

    ##### Cart Baru dari Pembeli
    @jwt_required
    def post(self):
        pembeli = get_jwt_claims()
        parse = reqparse.RequestParser()
        parse.add_argument('produk_id', location='args', required=True)
        parse.add_argument('qty', location='args', type=int,  required=True)
        
        args = parse.parse_args()

        produk = marshal(Produk.query.get(args['produk_id']), Produk.response_field)

        
        totalHarga = int(produk['harga'] * args['qty'])
        
        cart_baru = Cart(None, pembeli['id'], pembeli['username'], produk['id'], produk['namaProduk'], args['qty'],  totalHarga)
        db.session.add(cart_baru)
        db.session.commit()

        # return 
        return {"message": "INPUT CART SUCCESS", 'your cart': marshal(cart_baru, Cart.response_cart)}, 200, {'Content-Type': 'application/json'}
    
    ##### Melihat Cart dan Cart detail oleh Pembeli
    @jwt_required
    def get(self, idCart=None):
        pembeli = get_jwt_claims()
        
        if idCart == None:
            qry_cart = Cart.query.filter_by(pembeli_id=pembeli['id']).all()

            rows = []
            for row in qry_cart:
                temp = marshal(row, Cart.response_field)
                rows.append(temp)
            
            return rows, 200, {'Content-Type': 'application/json'}
        
        else:
            qry_cart = Cart.query.filter_by(pembeli_id=pembeli['id']).filter_by(id=idCart).first()
            if qry_cart is not None:
                return marshal(qry_cart, Cart.response_field), 200, {'Content-Type': 'application/json'}
            else:
                return {'status': 'NOT_FOUND'}, 404, {'Content-Type': 'application/json'}

    ##### EDIT Cart oleh Pembeli
    @jwt_required
    def put(self, idCart):
        pembeli = get_jwt_claims()
        
        qry_cart = Cart.query.filter_by(pembeli_id=pembeli['id']).filter_by(id=idCart).first()

        if qry_cart is None:
            return {'status': 'NOT_FOUND'}, 404, {'Content-Type': 'application/json'}

        else:
            cart = marshal(qry_cart, Cart.response_field)

            parse = reqparse.RequestParser()
            parse.add_argument('produk_id', location='args', default = cart['produk_id'])
            parse.add_argument('qty', location='args', type=int, default = cart['qty'])
            
            args = parse.parse_args()

            produk = marshal(Produk.query.get(args['produk_id']), Produk.response_field)
            
            totalHarga_baru = int(produk['harga'] * args['qty'])
            
            qry_cart.produk_id = args['produk_id']            
            qry_cart.namaProduk = produk['namaProduk']
            qry_cart.qty = args['qty']
            qry_cart.totalHarga = totalHarga_baru

            db.session.commit()
            return marshal(qry_cart, Cart.response_field), 200, {'Content-Type': 'application/json'}
    
    ##### HAPUS Cart oleh Penjual
    @jwt_required
    def delete(self, idCart):
        pembeli = get_jwt_claims()

        qry_cart = Cart.query.filter_by(pembeli_id = pembeli['id']).filter_by(id = idCart).first()

        if qry_cart is not None:
            db.session.delete(qry_cart)
            db.session.commit()
            return {'status': 'DATA_DELETED'}, 200, {'Content-Type': 'application/json'}
        else:
            return {'status': 'NOT_FOUND'}, 404, {'Content-Type': 'application/json'}

##### Endpoint Cart-Pembeli
api.add_resource(CartPembeli, '/pembeli/cart', '/pembeli/cart/<int:idCart>')   