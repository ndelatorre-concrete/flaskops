from datetime import datetime

from sqlalchemy.dialects.postgresql import ARRAY

from app.database import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=True)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(30), unique=True)
    address = db.Column(db.String(40), unique=True)


class Pizza(db.Model):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)
    ingredients = db.Column(ARRAY(db.String(20)), unique=True)


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime, nullable=True, default=datetime.now())
    delivered = db.Column(db.Boolean, nullable=False, default=False)

    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref=db.backref('orders', lazy='dynamic'))
