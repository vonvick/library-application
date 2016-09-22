# app/__init__.py


from flask import Flask
import os

app = Flask(__name__, instance_relative_config=True)

app.config.from_object(os.environ.get('APP_SETTINGS'))
# print(app.config.from_envvar('APP_SETTINGS'))
print(os.environ.get('APP_SETTINGS'))
# app.config.from_object('config.Config')
# app.config.from_pyfile('config.py', silent=True)

from app import controllers
