from blueprints import db
from flask_restful import fields

class Transaksi(db.Model):

    __tablename__ = "Transaksi"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True) # unique=True
    pembeli_id = db.Column(db.Integer, nullable=False)
    namaPembeli = db.Column(db.String(255), nullable=False)
    totalPembayaran = db.Column(db.Integer, nullable=False)    

    response_field = {
        'id': fields.Integer,
        'pembeli_id': fields.Integer,
        'namaPembeli': fields.String,
        'totalPembayaran': fields.Integer
    }


    def __init__(self, id, pembeli_id, namaPembeli, totalPembayaran):
        self.id = id
        self.pembeli_id = pembeli_id
        self.namaPembeli = namaPembeli
        self.totalPembayaran = totalPembayaran
        
    
    def __repr__(self): # return dari repr harus string
        return '<Transaksi %r>' %self.id
