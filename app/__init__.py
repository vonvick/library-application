# app/__init__.py

from flask import Flask
from .public import public
from .admin import admins


app = Flask(__name__)

# Puts the API blueprint.
app.register_blueprint(public, url_prefix = '/public')
app.register_blueprint(public, url_prefix = '/admin')
