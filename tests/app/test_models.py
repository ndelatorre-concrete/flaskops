from datetime import datetime

import pytest
from flask_sqlalchemy import event, SQLAlchemy as db

from app import bcrypt
from app.models import Order, Pizza, User
from tests.app import DatabaseTestCase


USER = User(id=1,
            name='Kristin Ortega',
            password=bcrypt.generate_password_hash('secret'),
            email='kristin.ortega@protectorium.com',
            address='Ground, district 589')


PIZZA = Pizza(id=1,
              name='Mexicana',
              price=10.00,
              ingredients=['nachos', 'pimenta'])


ORDER = Order(pizza_id=PIZZA.id,
              user_id=USER.id)


class OrderTestCase(DatabaseTestCase):
    def test_order_creation(self):



class PizzaTestCase(DatabaseTestCase):
    def test_pizza_creation(self):
        pass


class UserTestCase(DatabaseTestCase):
    def test_user_creation(self):
        pass
