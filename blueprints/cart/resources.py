import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from . import *
from blueprints import db
from blueprints.pembeli import Pembeli
from blueprints.produk import Produk
from blueprints.cart import Cart
from blueprints.transaksi import Transaksi
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_cart = Blueprint('Cart', __name__)
api = Api(bp_cart)


class CartPembeli(Resource):

    ##### Cart Baru dari Pembeli
    @jwt_required
    def post(self):
        pembeli = get_jwt_claims()
        if pembeli['status'] != 'pembeli':
            return {"status": "Unauthorized", "message": "Access Denied"}, 401, {'Content-Type': 'application/json'}

        parse = reqparse.RequestParser()
        parse.add_argument('produk_id', location='json', required=True)
        parse.add_argument('qty', location='json', type=int,  required=True)
        
        args = parse.parse_args()
        qry_produk = Produk.query.get(args['produk_id'])
        produk = marshal(qry_produk, Produk.response_field)

        if qry_produk.qty < args ['qty']:
            return {"status": "Not Acceptable", "message": "Not enough stock!"}, 406, {'Content-Type': 'application/json'}
        
        else:
            totalHarga = int(qry_produk.harga * args['qty'])
            status = 'unpaid'
            idTransaksi = 0
            sisa_produk = int(qry_produk.qty - args['qty'])
            
            cart_baru = Cart(None, pembeli['id'], pembeli['fullName'], produk['id'], produk['namaProduk'], produk['foto_produk'], args['qty'], produk['harga'], totalHarga, status, idTransaksi)
            db.session.add(cart_baru)
            qry_produk.qty = sisa_produk
            db.session.commit()               

            return {"status": "Created", "message": "Your cart has been created", 'cart': marshal(cart_baru, Cart.response_cart)}, 201, {'Content-Type': 'application/json'}
    
    ##### Melihat Cart dan Cart detail oleh Pembeli
    @jwt_required
    def get(self, idCart=None):
        pembeli = get_jwt_claims()
        if pembeli['status'] != 'pembeli':
            return {"status": "Unauthorized", "message": "Access Denied"}, 401, {'Content-Type': 'application/json'}
        
        if idCart == None:
            qry_cart = Cart.query.filter_by(pembeli_id=pembeli['id']).filter_by(status='unpaid')

            rows = []
            totalPayment = 0
            for row in qry_cart.all():
                totalPayment += row.totalHarga
                temp = marshal(row, Cart.response_cart)
                rows.append(temp)
            
            if qry_cart.first() is None:
                return {'status':'Not Found!', 'message': "You don't have any cart yet"}, 404, {'Content-Type': 'application/json'}
            else:
                return {'status':'OK', 'message':'Get all your cart', 'totalPayment': totalPayment, 'carts': rows}, 200, {'Content-Type': 'application/jason'}
        else:
            qry_cart = Cart.query.filter_by(pembeli_id=pembeli['id']).filter_by(id=idCart).first()
            if qry_cart is not None:
                cart = marshal(qry_cart, Cart.response_cart)
                return {'status':'OK', 'message':'Get a cart', 'cart': cart}, 200, {'Content-Type': 'application/jason'}

            else:
                return {'status':'Not Found!', 'message': 'DATA_NOT_FOUND'}, 404, {'Content-Type': 'application/json'}

    ##### HAPUS Cart oleh Penjual
    @jwt_required
    def delete(self, idCart):
        pembeli = get_jwt_claims()
        if pembeli['status'] != 'pembeli':
            return {"status": "Unauthorized", "message": "Access Denied"}, 401, {'Content-Type': 'application/json'}

        qry_cart = Cart.query.filter_by(pembeli_id = pembeli['id']).filter_by(id = idCart).first()
        cart = marshal(qry_cart, Cart.response_field)
        disp = marshal(qry_cart, Cart.response_cart)
        qry_produk = Produk.query.get(cart['produk_id'])

        produk = marshal(qry_produk, Produk.response_field)

        if qry_cart is not None:
            stock = (qry_produk.qty + cart['qty'])
            qry_produk.qty = stock
            db.session.delete(qry_cart)
            db.session.commit()
            return {'status':'OK', 'message': 'DATA_DELETED', 'cart': disp}, 200, {'Content-Type': 'application/json'}

        else:
            return {'status':'Not Found!', 'message': 'DATA_NOT_FOUND'}, 404, {'Content-Type': 'application/json'}

##### Endpoint Cart-Pembeli
api.add_resource(CartPembeli, '/pembeli/cart', '/pembeli/cart/<int:idCart>')   