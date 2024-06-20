# models.py
from extensions import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    contacts = db.relationship('Contact', backref='customer', lazy=True)
    opportunities = db.relationship('Opportunity', backref='customer', lazy=True)
    interactions = db.relationship('Interaction', backref='customer', lazy=True)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

class Opportunity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    stage = db.Column(db.String(50), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

class Interaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.String(500))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)