from app import current_app


@current_app.route('/')
def hello():
    return 'Hello World!'


@current_app.route('/orders')
def orders():
    return 'Lista de pedidos'


@current_app.route('/menu')
def menu():
    return 'Só tem Pepsi'
