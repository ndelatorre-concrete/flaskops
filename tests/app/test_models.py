from app.database import db
from app.models import Order, Pizza, User
from tests.app import DatabaseTestCase


USER = User(id=1,
            name='Kristin Ortega',
            password='123456',
            email='kristin.ortega@host.com',
            address='Ground, district 589')


PIZZA = Pizza(id=1,
              name='Mexicana',
              price=10.00,
              ingredients=['nachos', 'pimenta'])


ORDER = Order(pizza_id=PIZZA.id,
              user_id=USER.id)


class OrderTestCase(DatabaseTestCase):
    def test_order_creation(self):
        db.session.add_all([USER, PIZZA, ORDER])
        db.session.commit()

        persisted_order = Order.query.filter_by(id=ORDER.id).first()
        self.assertEqual(persisted_order, ORDER)


class PizzaTestCase(DatabaseTestCase):
    def test_pizza_creation(self):
        db.session.add(PIZZA)
        db.session.commit()

        persisted_pizza = Pizza.query.filter_by(id=Pizza.id).first()
        self.assertEqual(persisted_pizza, PIZZA)


class UserTestCase(DatabaseTestCase):
    def test_user_creation(self):
        db.session.add(USER)
        db.session.commit()

        persisted_user = User.query.filter_by(id=User.id).first()
        self.assertEqual(persisted_user, USER)
