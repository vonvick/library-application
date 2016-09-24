#!flask/bin/python

from app import app
import os

# app.debug = True
if os.environ.get('APP_SETTINGS') == 'config.DevelopmentConfig':
    app.run()