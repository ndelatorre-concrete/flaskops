from flask import Flask, jsonify
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager


app = Flask(__name__)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)


from app.views import *
from app.database import db_session


@app.teardown_appcontext
def shutdown_session(*_):
    """
    Shutdown a db session opened for a closed web request.
    :param _:
    :return:
    """
    db_session.remove()


@app.errorhandler(404)
def page_not_found(*_):
    return jsonify(error=404, text='Resource not found'), 404


@login_manager.unauthorized_handler
def unauthorized():
    return jsonify(error=402, text='Unauthorized'), 402
