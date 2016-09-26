# app/__init__.py

from flask import Flask
import os


app = Flask(__name__)

app.config.from_object(os.environ.get('APP_SETTINGS'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from .controllers import public, admin

app.register_blueprint(public.mod, url_prefix='')
app.register_blueprint(admin.mod, url_prefix='/admin')


from .models import User