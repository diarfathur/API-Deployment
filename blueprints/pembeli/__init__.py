from blueprints import db
from flask_restful import fields

class Pembeli(db.Model):

    __tablename__ = "Pembeli"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True) # unique=True
    username = db.Column(db.String(20), unique = True)
    password = db.Column(db.String(20), nullable = False)
    contact = db.Column(db.String(15), nullable = False)
    status = db.Column(db.String(7), nullable = False)
    email = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(500), nullable=False)


    response_field = {
        'id': fields.Integer,
        'username': fields.String,
        'password': fields.String,
        'contact': fields.String,
        'status': fields.String,
        'email': fields.String,
        'address': fields.String
    }

    response_token = {
        'id': fields.Integer,
        'username': fields.String,
        'status': fields.String
    }

    response_pembeli = {
        'username': fields.String,
        'contact': fields.String,
        'status': fields.String,
        'email': fields.String,
        'address': fields.String
    }

    def __init__(self, id, username, password, contact, status, email, address):
        self.id = id
        self.username = username
        self.password = password
        self.contact = contact
        self.status = status
        self.email = email
        self.address = address
    
    def __repr__(self): # return dari repr harus string
        return '<Pembeli %r>' %self.id
    