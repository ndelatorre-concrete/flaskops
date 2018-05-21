from unittest import TestCase

from sqlalchemy import event

from app.config import TestConfig
from app.database import db
from app.factory import create_app


class DatabaseTestCase(TestCase):
    def __start_transaction(self):
        # Create a db session outside of the ORM that we can roll back
        self.connection = db.engine.connect()
        self.trans = self.connection.begin()

        # bind db.session to that connection, and start a nested transaction
        db.session = db.create_scoped_session(options={'bind': self.connection})
        db.session.begin_nested()

        # sets a listener on db.session so that whenever the transaction ends-
        # commit() or rollback() - it restarts the nested transaction
        @event.listens_for(db.session, "after_transaction_end")
        def restart_savepoint(session, transaction):
            if transaction.nested and not transaction._parent.nested:
                session.begin_nested()

        self.__after_transaction_end_listener = restart_savepoint

    def __close_transaction(self):
        # Remove listener
        event.remove(db.session, "after_transaction_end", self.__after_transaction_end_listener)

        # Roll back the open transaction and return the db connection to
        # the pool
        db.session.close()

        # The app was holding the db connection even after the session was closed.
        # This caused the db to run out of connections before the tests finished.
        # Disposing of the engine from each created app handles this.
        db.get_engine(self.app).dispose()

        self.trans.rollback()
        self.connection.invalidate()

    def setUp(self):
        super().setUp()
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.init_app(self.app)
        self.__start_transaction()

    def tearDown(self):
        super().tearDown()
        self.__close_transaction()
        self.app_context.pop()
