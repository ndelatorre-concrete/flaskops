from os import path


class BaseConfig(object):

    PROJECT = "flaskops"

    # Get app root path, also can use flask.root_path.
    # ../../config.py
    PROJECT_ROOT = path.abspath(path.dirname(path.dirname(__file__)))

    DEBUG = False
    TESTING = False

    ADMINS = ['youremail@yourdomain.com']

    # http://flask.pocoo.org/docs/quickstart/#sessions
    SECRET_KEY = 'secret key'

    LOG_FOLDER = '/tmp/flaskops/logs'


class DefaultConfig(BaseConfig):
    DEBUG = True

    # Flask-Sqlalchemy: http://packages.python.org/Flask-SQLAlchemy/config.html
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'postgres://flaskops:flaskops@127.0.0.1/flaskops'


class TestConfig(BaseConfig):
    TESTING = True

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'postgres://flaskops:flaskops@127.0.0.1/flaskops_test'
