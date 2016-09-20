# app/__init__.py
<<<<<<< HEAD
from flask import Flask

app = Flask(__name__)

from app import controllers
=======

from flask import Flask
from .public import public
from .admin import admin


app = Flask(__name__)
app.config.from_object('app.admin.config')

# Puts the API blueprint.
app.register_blueprint(public, url_prefix = '/public')
app.register_blueprint(admin, url_prefix = '/admin')
>>>>>>> 9bceb7515570fce8e93504ca4b8012168234248b
