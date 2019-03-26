from blueprints import db
from flask_restful import fields

class Cart(db.Model):

    __tablename__ = "Cart"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True) # unique=True
    idTransaksi = db.Column(db.Integer, nullable=False)
    pembeli_id = db.Column(db.Integer, nullable=False)
    namaPembeli = db.Column(db.String(255), nullable=False)
    produk_id = db.Column(db.Integer, nullable=False)
    namaProduk = db.Column(db.String(255), nullable=False)
    gambarProduk = db.Column(db.String(255), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    hargaSatuan = db.Column(db.Integer, nullable=False)
    totalHarga = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(10), nullable=False)
    

    response_field = {
        'id': fields.Integer,
        'idTransaksi': fields.Integer,
        'pembeli_id': fields.Integer,
        'namaPembeli': fields.String,
        'produk_id': fields.Integer,
        'namaProduk': fields.String,
        'gambarProduk': fields.String,
        'qty': fields.Integer,
        'hargaSatuan': fields.Integer,
        'totalHarga': fields.Integer,
        'status': fields.String,
    }

    response_cart = {
        'id': fields.Integer,
        'idTransaksi': fields.Integer,
        'namaPembeli': fields.String,
        'namaProduk': fields.String,
        'gambarProduk': fields.String,
        'qty': fields.Integer,
        'hargaSatuan': fields.Integer,
        'totalHarga': fields.Integer,
        'status': fields.String
    }

    def __init__(self, id, pembeli_id, namaPembeli, produk_id, namaProduk, gambarProduk, qty, hargaSatuan, totalHarga, status, idTransaksi):
        self.id = id
        self.pembeli_id = pembeli_id
        self.namaPembeli = namaPembeli
        self.produk_id = produk_id
        self.namaProduk = namaProduk
        self.gambarProduk = gambarProduk
        self.qty = qty
        self.hargaSatuan = hargaSatuan
        self.totalHarga = totalHarga
        self.status = status
        self.idTransaksi = idTransaksi
        
    
    def __repr__(self): # return dari repr harus string
        return '<Cart %r>' %self.id
