from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, Float, ForeignKey, String
from sqlalchemy.orm import backref, relationship
from sqlalchemy.dialects.postgresql import ARRAY

from app.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=True)
    password = Column(String(60), nullable=False)
    email = Column(String(30), unique=True)
    address = Column(String(40), unique=True)


class Pizza(Base):
    __tablename__ = 'pizzas'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    price = Column(Float, nullable=False)
    ingredients = Column(ARRAY(String(20)), unique=True)


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, nullable=True, default=datetime.now())
    delivered = Column(Boolean, nullable=False, default=False)

    pizza_id = Column(Integer, ForeignKey('pizza.id'))

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', backref=backref('orders', lazy='dynamic'))
