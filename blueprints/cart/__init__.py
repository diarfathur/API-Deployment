from blueprints import db
from flask_restful import fields

class Cart(db.Model):

    __tablename__ = "Cart"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True) # unique=True
    pembeli_id = db.Column(db.Integer, nullable=False)
    namaPembeli = db.Column(db.String(255), nullable=False)
    produk_id = db.Column(db.Integer, nullable=False)
    namaProduk = db.Column(db.String(255), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    totalHarga = db.Column(db.Integer, nullable=False)
    
    response_field = {
        'id': fields.Integer,
        'pembeli_id': fields.Integer,
        'namaPembeli': fields.String,
        'produk_id': fields.Integer,
        'namaProduk': fields.String,
        'qty': fields.Integer,
        'totalHarga': fields.Integer
    }

    response_cart = {
        'namaPembeli': fields.String,
        'namaProduk': fields.String,
        'qty': fields.Integer,
        'totalHarga': fields.Integer
    }

    def __init__(self, id, pembeli_id, namaPembeli, produk_id, namaProduk, qty, totalHarga):
        self.id = id
        self.pembeli_id = pembeli_id
        self.namaPembeli = namaPembeli
        self.produk_id = produk_id
        self.namaProduk = namaProduk
        self.qty = qty
        self.totalHarga = totalHarga
        
    
    def __repr__(self): # return dari repr harus string
        return '<Cart %r>' %self.id
