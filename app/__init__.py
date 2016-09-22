# app/__init__.py


from flask import Flask
import os

app = Flask(__name__)
# app.config.from_object(os.environ['APP_SETTINGS'])
# print(os.environ['APP_SETTINGS'])
app.config.from_object('config')

from app import controllers
