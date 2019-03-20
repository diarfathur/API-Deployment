from blueprints import db
from flask_restful import fields


class Penjual(db.Model):
    __tablename__ = "Penjual"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True) # unique=True
    username = db.Column(db.String(20), unique = True)
    password = db.Column(db.String(20), nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    status = db.Column(db.String(7), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(500), nullable=False)
    foto_profil = db.Column(db.String(100))
    deskripsi_penjual = db.Column(db.String(100))
    # date_joined = db.Column(db.DateTime)

    response_field = {
        'id': fields.Integer,
        'username': fields.String,
        'password': fields.String,
        'contact': fields.String,
        'status': fields.String,
        'email': fields.String,
        'address': fields.String,
        'foto_profil': fields.String,
        'deskripsi_penjual': fields.String
    }

    response_token = {
        'id': fields.Integer,
        'username': fields.String,
        'status': fields.String
    }

    response_penjual = {
        'username': fields.String,
        'contact': fields.String,
        'status': fields.String,
        'email': fields.String,
        'address': fields.String,
        'foto_profil': fields.String,
        'deskripsi_penjual': fields.String
    }

    def __init__(self, id, username, password, contact, status, email, address, foto_profil, deskripsi_penjual): #, address, foto_profil, deskripsi_penjual):
        self.id = id
        self.username = username
        self.password = password
        self.contact = contact
        self.status = status
        self.email = email
        self.address = address
        self.foto_profil = foto_profil
        self.deskripsi_penjual = deskripsi_penjual

    
    def __repr__(self): # return dari repr harus string
        return '<Penjual %r>' %self.id