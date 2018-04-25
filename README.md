# FlaskOps

Uma aplicação REST simples para passar conhecimento de Flask e WebAPI para o time de DevOps da Concrete :)

---

# Parte I - Ambiente e roteamento

###  Admirável ambiente novo - configuração de um novo ambiente ambiente para um novo projeto

* Versão - *pyenv*
A primeira coisa a decidir quando se inicia um novo projeto Python é sua versão. Um fator crucial para essa decisão vem das libs que você utilizará. Raras vezes uma lib (estranha) que você quer usar ainda não é compatível com as últimas versões de Python.
Felizmente, se você for usar libs de propósito genérico, provavelmente ela já está pronta para executar com as últimas versões de Python. \o/
Vamos listar as versões de Python que meu `pyenv` possui, e então setar a mais recente:

```sh
    $ pyenv versions
      system
    * 3.6.3 (set by /home/ndelatorre/.pyenv/version)
      3.6.4
    $ pyenv global 3.6.4
    $ pyenv versions
      system
      3.6.3
    * 3.6.4 (set by /home/ndelatorre/.pyenv/version)
    $ python --version
    Python 3.6.4
```

* Ambiente virtual - *virtualenv*
Ambientes virtuais são caixinhas de areia para seus apps não brigarem querendo o mesmo brinquedo (lib) de cores (versões) diferentes. Assim que você definir a versão, crie um novo ambiente virtual com `virtualenv`. Não se esqueça de ativar o ambiente virtual, comumentemente feito com `source`. Note que o nome do diretório do ambiente virtual aparece no terminal antes do caret entre parênteses:

```sh
    $ virtualenv ~/.venv/flaskops
    Using base prefix '/home/ndelatorre/.pyenv/versions/3.6.4'
    New python executable in /home/ndelatorre/.venv/flaskops/bin/python3.6
    Also creating executable in /home/ndelatorre/.venv/flaskops/bin/python
    Installing setuptools, pip, wheel...done.
    $ source ~/.venv/flaskops/bin/activate
    (flaskops) $ which python
    /home/ndelatorre/.venv/flaskops/bin/python
```

* Gerenciador de Pacotes - *pip*
Agora você tem a caixinha (ambiente), mas ainda está sem brinquedos (libs) :(
Peça um frasco para o `pip`, seu gerenciador de pacotes! Ele cuidará das dependências de todas as libs que você pedir para ele :)
Give that program a beer!

```sh
    (flaskops) $ pip install flask
    Collecting flask
      Downloading https://files.pythonhosted.org/packages/77/32/e3597cb19ffffe724ad4bf0beca4153419918e7fa4ba6a34b04ee4da3371/Flask-0.12.2-py2.py3-none-any.whl (83kB)
        100% |████████████████████████████████| 92kB 337kB/s
    Collecting itsdangerous>=0.21 (from flask)
      Downloading https://files.pythonhosted.org/packages/dc/b4/a60bcdba945c00f6d608d8975131ab3f25b22f2bcfe1dab221165194b2d4/itsdangerous-0.24.tar.gz (46kB)
        100% |████████████████████████████████| 51kB 392kB/s
    Collecting click>=2.0 (from flask)
      Downloading https://files.pythonhosted.org/packages/34/c1/8806f99713ddb993c5366c362b2f908f18269f8d792aff1abfd700775a77/click-6.7-py2.py3-none-any.whl (71kB)
        100% |████████████████████████████████| 71kB 796kB/s
    Collecting Jinja2>=2.4 (from flask)
      Downloading https://files.pythonhosted.org/packages/7f/ff/ae64bacdfc95f27a016a7bed8e8686763ba4d277a78ca76f32659220a731/Jinja2-2.10-py2.py3-none-any.whl (126kB)
        100% |████████████████████████████████| 133kB 650kB/s
    Collecting Werkzeug>=0.7 (from flask)
      Downloading https://files.pythonhosted.org/packages/20/c4/12e3e56473e52375aa29c4764e70d1b8f3efa6682bef8d0aae04fe335243/Werkzeug-0.14.1-py2.py3-none-any.whl (322kB)
        100% |████████████████████████████████| 327kB 655kB/s
    Collecting MarkupSafe>=0.23 (from Jinja2>=2.4->flask)
    Building wheels for collected packages: itsdangerous
      Running setup.py bdist_wheel for itsdangerous ... done
      Stored in directory: /home/ndelatorre/.cache/pip/wheels/2c/4a/61/5599631c1554768c6290b08c02c72d7317910374ca602ff1e5
    Successfully built itsdangerous
    Installing collected packages: itsdangerous, click, MarkupSafe, Jinja2, Werkzeug, flask
    Successfully installed Jinja2-2.10 MarkupSafe-1.0 Werkzeug-0.14.1 click-6.7 flask-0.12.2 itsdangerous-0.24
```

---

# Talk tech to me, baby - Roteamento

Vamos transformar aquele "Hello World" numa API com mais de 2 neurônios: escrever funções e organizar o Flask para responder em dois end-points (;

Antes de montar o Frank, vamos entender cada peça do "Hello World". Aqui está ele:

```python
    from flask import Flask  # do pacote 'flask', importe a classe Flask
    app = Flask(__name__)   # Instancia um Flask, passando um valor que ele usará para saber onde estão seus arquivos (explico o __name__ numa próxima, ok?)


    @app.route('/')  # Faz com que o Flask 'app' execute essa função todas as vezes que ele resolver a rota '/'
    def hello():
        return 'Hello World!'  # retorna um body com `Hello World!`
```

"É só isso?" Sim, é só isso. E agora, teremos mais 2 end-points com os seguintes propósitos:

* Lista e realiza pedidos:
```python
    @app.route('/orders')
    def orders():
        return 'Lista de pedidos'
```

* Mostra o cardápio:
```python
    @app.route('/menu')
    def menu():
        return 'Só tem Pepsi'
```

Estamos falando e sendo respondidos \o/
Porém, ainda apenas no Mundo das Ideias :(

---

# Haja Luz

Vamos subir o servidor e tentar falar nesses end-points que criamos. Com o `virtualenv` que criamos e instalamos o flask ativado, vamos pedir ajuda à ele:

```sh
    $ flask --help
    Usage: flask [OPTIONS] COMMAND [ARGS]...

      This shell command acts as general utility script for Flask applications.

      It loads the application configured (through the FLASK_APP environment
      variable) and then provides commands either provided by the application or
      Flask itself.

      The most useful commands are the "run" and "shell" command.

      Example usage:

        $ export FLASK_APP=hello.py
        $ export FLASK_DEBUG=1
        $ flask run

    Options:
      --version  Show the flask version
      --help     Show this message and exit.

    Commands:
      run    Runs a development server.
      shell  Runs a shell in the app context.
```

Hmm, `flask run` parece subir o Frank:

```sh
    $ flask run
    Usage: flask run [OPTIONS]

    Error: Could not locate Flask application. You did not provide the FLASK_APP environment variable.
```

Ops, parece que o Flask precisa saber onde está o módulo onde instaciamos o objeto `Flask`. Ele está em `./app.__init__.py`:

```sh
    (flaskops) ndelatorre@~/Projects/flaskops - [part_I]
    $ export FLASK_APP=./app/__init__.py
    (flaskops) ndelatorre@~/Projects/flaskops - [part_I]
    $ flask run
     * Serving Flask app "app"
     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Ou apenas:

```sh
    (flaskops) ndelatorre@~/Projects/flaskops - [part_I]
    $ FLASK_APP="./app/__init__.py" flask run
```

Teste em:

[http://127.0.0.1:5000/](http://127.0.0.1:5000/)
[http://127.0.0.1:5000/orders](http://127.0.0.1:5000/orders)
[http://127.0.0.1:5000/menu](http://127.0.0.1:5000/menu)

---

# Não deixe nada faltando

Para que você possa passar o projeto para outra máquina sem o mesmo ambiente e/ou sem as mesmas libs, existe o salvador (e, às vezes, confuso), `requirements.txt`. Nele, você pode deixar listada todas as libs e suas versões que o seu projeto está usando, e o nosso parça `pip` faz a camaradagem de listar ou instalar dali tudo se você pedir:


* Para listar suas libs
```sh
    pip freeze
```

* Para jogar no `requirements.txt`
```sh
    pip freeze > requirements.txt
```

* Para instalar tudo o que estiver no `requirements.txt`
*
```sh
    pip install -r requirements.txt
```
