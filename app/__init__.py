# app/__init__.py

from flask import Flask
from .public import public


app = Flask(__name__)

# Puts the API blueprint on api.U2FtIEJsYWNr.com.
app.register_blueprint(public, url_prefix = '/public')