from flask.ext.login import login_required

from app import app


@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/orders')
@login_required
def orders():
    return 'Lista de pedidos'


@app.route('/menu')
def menu():
    return 'Só tem Pepsi'
