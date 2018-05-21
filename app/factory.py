from flask import Flask

from app.config import DefaultConfig
from app.database import db

__all__ = ['create_app']


def create_app(config=None, app_name=None):
    """Cria uma aplicação Flask."""

    if app_name is None:
        app_name = DefaultConfig.PROJECT

    app = Flask(app_name)
    configure_app(app, config)
    configure_error_handlers(app)

    return app


def configure_app(app, config_object=None):
    """Possibilita configurações para teste e produção."""

    if config_object:
        app.config.from_object(config_object)
        return

    # http://flask.pocoo.org/docs/api/#configuration
    app.config.from_object(DefaultConfig)


def configure_extensions(app):
    # flask-sqlalchemy
    db.init_app(app)


# http://flask.pocoo.org/docs/latest/errorhandling/
def configure_error_handlers(app):

    @app.errorhandler(404)
    def page_not_found(error):
        return 'Not found', 404
