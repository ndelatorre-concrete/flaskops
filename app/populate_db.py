"""
Esse módulo é apenas para inserção na base de dev e homolog e não deve fazer parte da branch de prod
"""

from app.models import Pizza, User


PIZZAS = [
    Pizza(name='4 queijos', price=0.00, ingredients=['mussarela', 'provolone', 'parmessão', 'gorgonzola',]),
    Pizza(name='Bahiana', price=0.00, ingredients=['mussarela', 'calabresa', 'pimenta', 'cebola',]),
    Pizza(name='Calabresa', price=0.00, ingredients=['mussarela', 'calabresa',]),
]


USERS = [
    User(name='test_user', password='secret', email='nome.sobrenome@host.com', address='Rua Springfield, 42')
]
