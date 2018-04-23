from flask import Flask, jsonify

app = Flask(__name__)


from app.views import *


@app.errorhandler(404)
def page_not_found(*_):
    return jsonify(error=404, text='Resource not found'), 404
