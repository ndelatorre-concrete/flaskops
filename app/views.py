from app import app


@app.route('/')
def hello():
    return 'Benvindos ao FlaskOps'


@app.route('/orders')
def orders():
    return 'Lista de pedidos'


@app.route('/menu')
def menu():
    return 'Só tem Pepsi'
