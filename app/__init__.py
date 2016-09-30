# app/__init__.py

import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ.get('APP_SETTINGS'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from app.controllers.admin import admin
from app.controllers.public import public
from app import models
from .models import Users


app.register_blueprint(admin)
app.register_blueprint(public)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'public.login'

@login_manager.user_loader
def load_user(user_id):
    user = Users.query.get(int(user_id))
    return user

