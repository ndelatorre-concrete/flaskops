# Parte II - Estrutura e Modelos


*** Init DB

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
/home/ndelatorre/.venv/flaskops/lib/python3.6/site-packages/psycopg2/__init__.py:144: UserWarning: The psycopg2 wheel package will be renamed from release 2.8; in order to keep installing from binary please use "pip install psycopg2-binary" instead. For details see: <http://initd.org/psycopg/docs/install.html#binary-install-from-pypi>.
  """)
```python

---