from blueprints import db
from flask_restful import fields

class Produk(db.Model):

    __tablename__ = "Produk"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True) # unique=True
    penjual_id = db.Column(db.Integer, nullable=False)
    penjual = db.Column(db.String(255), nullable=False)
    namaProduk = db.Column(db.String(255), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    harga = db.Column(db.Integer, nullable=False)
    kategori = db.Column(db.String(50), nullable=False)
    foto_produk = db.Column(db.String(500), nullable=False)
    deskripsi_produk = db.Column(db.Text, nullable=False)
    # status = db.Column(db.)
    
    
    response_field = {
        'id': fields.Integer,
        'penjual_id': fields.Integer,
        'penjual': fields.String,
        'namaProduk': fields.String,
        'qty': fields.Integer,
        'harga': fields.Integer,
        'kategori': fields.String,
        'foto_produk': fields.String,
        'deskripsi_produk': fields.String
    }

    response_public = {
        'id': fields.Integer,
        'penjual': fields.String,
        'namaProduk': fields.String,
        'qty': fields.Integer,
        'harga': fields.Integer,
        'kategori': fields.String,
        'foto_produk': fields.String,
        'deskripsi_produk': fields.String
    }

    def __init__(self, id, penjual_id, penjual, namaProduk, qty, harga, kategori, foto_produk, deskripsi_produk):
        self.id = id
        self.penjual_id = penjual_id
        self.penjual = penjual
        self.namaProduk = namaProduk
        self.qty = qty
        self.harga = harga
        self.kategori = kategori
        self.foto_produk = foto_produk
        self.deskripsi_produk = deskripsi_produk
        
    
    def __repr__(self): # return dari repr harus string
        return '<Produk %r>' %self.id
