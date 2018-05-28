# Parte II - Estrutura e Modelos

###  Organizando a casa

Nosso app funciona, mas ele está engessado para sempre executar com as mesmas configurações. Isso não é legal para migrar e muito menos para testar. E migrar sem testar é mais feio que bater na mãe, então vamos mudar isso:

##### Definindo as configurações

O `Flask()` aceita ter seus atributos configurados a partir de atributos de outra uma classe. Assim:

```python
class FlaskConfig:
    DEBUG = True

config_object = FlaskConfig()
app = Flask()
app.config.from_object(config_object)
```

Hmmm, esse `Config` tem potencial... Vamos criar um  módulo cheio desses, um para cada necessidade. Aqui vai uma parte do código desse módulo pra ficar menos abstrato o *como* vamos usufruir dessas configurações diferentes. Dá uma olhada nos `SQLALCHEMY_DATABASE_URI`, e relaxa que já vamos falar sobre essas variáveis :yum:

[app.config](https://github.com/ndelatorre-concrete/flaskops/tree/part_II/app/config.py)
```python
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
```
---

##### A todo vapor

Para criar `Flask()`s com `Config` diferentes, vamos usar o famoso Design Pattern `Factory`, de maneira que pediremos sempre para a mesma função `create_app` criar para a gente `Flask()`s com as configurações que pedirmos:

[app.factory](https://github.com/ndelatorre-concrete/flaskops/blob/part_II/app/factory.py)
```python
def create_app(config=None, app_name=None):
    """Cria uma aplicação Flask."""

    if app_name is None:
        app_name = DefaultConfig.PROJECT

    app = Flask(app_name)
    configure_app(app, config)  # configura variáveis referente a caminhos, testes, bibliotecas, etc
    configure_error_handlers(app)  # decora funções a serem executadas caso ocorra um erro (404, 500, etc)

    return app
```

Então nosso [app/\_\_init\_\_.py](https://github.com/ndelatorre-concrete/flaskops/tree/part_II/app/__init__.py) ficou apenas invocando o `app.factory.create_app`, sem passar argumento algum, para que o app seja instanciado da maneira definida como padrão. Infelizmente esse app fica global na `app.current_app`, pois precisamos de uma app para rotear as views (lembra do `@app.route('/path')`?), mas isso seria uma outra história se fossemos usar [Blueprints](http://flask.pocoo.org/docs/1.0/blueprints/).

---
### Call 'em Models

Para o Flaskops lembrar dos seus usuáris, seus pedidos, cardápio, etc, ele precisa de um banco de dados, e [PostgreSQL](https://www.postgresql.org/) é um queridinho de nós Pythonistas.

Eu usei Docker na máquina local, mas você pode fazer como quiser. Vamos precisar de dois bancos, um para testes e outro para "prod". Para facilitar, o user, a senha e o nome da base são todos *flaskops*, ouvindo na porta padrão do PostgreSQL "5432". Então ficou assim:

```sh
sudo docker run --name postgres-flaskops -e POSTGRES_PASSWORD=flaskops -p 5432:5432 -d postgres
```

Um cli-client bastante usado para PostgreSQL é o [psql](http://postgresguide.com/utilities/psql.html).

```sh
sudo apt-get install postgresql
```

E você conecta ao seu novo contêiner assim como usuário `postgres` (default) no banco `postgres` (default):

```sh
psql -h 127.0.0.1 -p 5432 -U postgres -W postgres
```

Ele vai pedir a senha do usuário `postgres` (aquela que você colocou em `POSTGRES_PASSWORD`). Então, crie os bancos e o usuário:

```sql
CREATE DATABASE flaskops;
CREATE DATABASE flaskops_test;

CREATE USER flaskops WITH PASSWORD 'flaskops';

GRANT ALL PRIVILEGES ON DATABASE flaskops to flaskops;
GRANT ALL PRIVILEGES ON DATABASE flaskops_test to flaskops;
```
---

Okay, agora temos onde guardar os dados. Vamos à parte legal:

##### SQLAlchemy, seu amigão ORM:

Um SQLAlchemy serve basicamente para traduzir suas queries de python para SQL. Ele também transforma suas classes em tabelas, seus atributos em colunas e lida com as sessões e mais uma porção de coisa legal que não precisaremos para pedir pizza.

Instale o `flask_sqlalchemy` com o pip:

```sh
pip install flask_sqlalchemy
```

Instancie um SQLAlchemy para conseguir atrelar classes à nossas futuras tabelas na nossa base novinha. Crie um módulo em `app/database.py`:

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
```

Fazendo isso, vamos conseguir modularizar o nosso `db` de maneira que conseguimos conectar esse a nossa base e outro a outra base, se um dia tivermos mais de uma. Não iremos nesse caso, mas essa é uma boa prática e deixa mais limpo o nosso `app/__init__.py`.

Atrelamos o `db` ao nosso app em [app.config.configure_extensions](https://github.com/ndelatorre-concrete/flaskops/blob/part_II/app/config.py):

```python
from app.database import db

...

def configure_extensions(app):
    # flask-sqlalchemy
    db.init_app(app)
```
---

##### Show me the data, sire!

Em [app.models](https://github.com/ndelatorre-concrete/flaskops/blob/part_II/app/models.py) vamos criar classes que representarão nossas tabelas, e seus atributos, as colunas dessas tabelas. Assim, uma linha do banco pode ser representar por uma instância dessa classe. Tipo assim:

```python
pizza_de_quatro_queijos = Pizza(name='4 queijos', price=0.00, ingredients=['mussarela', 'provolone', 'parmessão', 'gorgonzola',])
```
 Bora lá em [app.models](https://github.com/ndelatorre-concrete/flaskops/blob/part_II/app/models.py):


```python
class User(db.Model):  # nosso `db` do app.database
    __tablename__ = 'users'  # nome da tabela equivalente à essa classe no banco

    id = db.Column(db.Integer, primary_key=True)  # para fazermos colunas na tabela, precisamos de atributos do tipo db.Column. Este, por sua vez, precisa saber ao menos que tipo de dado guardará (uma db.Integer, nesse caso)
    name = db.Column(db.String(40), nullable=True)  # para aparecer em msg de "benvindo"
    password = db.Column(db.String(60), nullable=False)  # _
    email = db.Column(db.String(30), unique=True)  # para login e log das ações que possam interessar ao usuário
    address = db.Column(db.String(40), unique=True)  # onde ele quer receber seus pedidos


class Pizza(db.Model):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)
    ingredients = db.Column(ARRAY(db.String(20)), unique=True)  # Uma lista de strings


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime, nullable=True, default=datetime.now())  # quando esse pedido foi feito?
    delivered = db.Column(db.Boolean, nullable=False, default=False)  # esse pedido foi entregue?

    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id')) # pediu qual pizza?

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # quem pediu?
    user = db.relationship('User', backref=db.backref('orders', lazy='dynamic'))
```

Escrevemos bastante, mas isso ainda nem tocou o banco :(
Para criar nossas tabelas, colunas, indexes, constraints, etc. no banco, basta chamarmos a função `db.create_all()`

# TODO explain this shit, god damn

```python
Python 3.6.4 (default, Apr 18 2018, 13:33:33)
[GCC 6.3.0 20170516] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from app.factory import create_app
>>> from app.config import TestConfig
>>> app = create_app(TestConfig)
>>> from app.database import db
>>> from app.models import *
>>> app.app_context().push()
>>> db.init_app(app)
>>> db.create_all()
```

Com esses dados, conseguiremos fazer nosso web-app sem maiores problemas e/ou sofisticações desnecessárias para um "MVP". Chegou a hora em @ filh@ chora e a mãe não vê.

---

### Prova dos 9 pytheira

# TODO HAHAHAHHA



















