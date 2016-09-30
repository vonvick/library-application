#!flask/bin/python


import os
from app import app


if os.environ.get('APP_SETTINGS') == 'config.DevelopmentConfig':
    app.run()

