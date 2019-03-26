import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from . import *
from blueprints import db
from blueprints.pembeli import Pembeli
from blueprints.cart import Cart
from blueprints.transaksi import Transaksi
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_transaksi = Blueprint('Transaksi', __name__)
api = Api(bp_transaksi)


class TransaksiPembeli(Resource):

    ##### Cart Baru dari Pembeli
    @jwt_required
    def post(self):
        pembeli = get_jwt_claims()
        if pembeli['status'] != 'pembeli':
            return {"status": "Unauthorized", "message": "Access Denied"}, 401, {'Content-Type': 'application/json'}

        qry_cart = Cart.query.filter_by(pembeli_id=pembeli['id']).filter_by(status='unpaid').filter_by(idTransaksi=0)
        totalPembayaran = 0
        if qry_cart.first() is None:
            return {"status": "Bad Request", "message": "You haven't any unpaid cart"}, 400, {'Content-Type': 'application/json'}

        else:
            for temp in qry_cart.all():
                totalPembayaran += temp.totalHarga
            
            tr = Transaksi(None, pembeli['id'], pembeli['fullName'], totalPembayaran)
            db.session.add(tr)
            db.session.commit()

            cartList = []
            for cart in qry_cart:
                cart.idTransaksi = tr.id
                cart.status = "paid"
                cart = marshal(cart, Cart.response_cart)
                cartList.append(cart)
            db.session.commit()

            transaksi = marshal(tr, Transaksi.response_field)
            return {"status": "Accepted", "message": "Your transaction is success", 'transaction': transaksi, 'carts': cartList}, 202, {'Content-Type': 'application/json'}
    
    ##### Melihat Cart dan Cart detail oleh Pembeli
    @jwt_required
    def get(self, idTransaksi=None):
        pembeli = get_jwt_claims()
        if pembeli['status'] != 'pembeli':
            return {"status": "Unauthorized", "message": "Access Denied"}, 401, {'Content-Type': 'application/json'}
        
        if idTransaksi == None:
            qry_transaksi = Transaksi.query.filter_by(pembeli_id=pembeli['id']).all()
            
            transaksi = []
            cartList = []
            for row in qry_transaksi:
                qry_cart = Cart.query.filter_by(idTransaksi=row.id).all()
                
                for cart in qry_cart:
                    tempCart = marshal(cart, Cart.response_cart)
                    cartList.append(tempCart)
                
                temp = marshal(row, Transaksi.response_field)
                temp['details'] = cartList
                transaksi.append(temp)
                cartList = []
            
            return {'status':'OK', 'message':'Your All Transactions', 'transactions': transaksi}, 200, {'Content-Type': 'application/jason'}
        
        else:
            qry_transaksi = Transaksi.query.filter_by(pembeli_id=pembeli['id']).filter_by(id=idTransaksi).first()
            qry_cart = Cart.query.filter_by(idTransaksi=idTransaksi).all()
            cartList = []
            for cart in qry_cart:
                tempCart = marshal(cart, Cart.response_cart)
                cartList.append(tempCart)

            if qry_transaksi is not None:
                transaksi = marshal(qry_transaksi, Transaksi.response_field)
                return {'status':'OK', 'message':'Your Transaction', 'transaction': transaksi, 'cartList': cartList}, 200, {'Content-Type': 'application/jason'}

            else:
                return {'status':'Not Found!', 'message': 'DATA_NOT_FOUND'}, 404, {'Content-Type': 'application/json'}

    ##### Endpoint Cart-Pembeli
api.add_resource(TransaksiPembeli, '/pembeli/transaksi', '/pembeli/transaksi/<int:idTransaksi>')   