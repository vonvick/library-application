# config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL')
    GOOGLE_LOGIN_CLIENT_ID = "10894599167-7su82sutnhudiase1isrloi1s2ivc41u.apps.googleusercontent.com"
    GOOGLE_LOGIN_CLIENT_SECRET = "qiZ1SM_dfDlTG11Hfso1Xmdy"

    OAUTH_CREDENTIALS={
        'google': {
            'id': GOOGLE_LOGIN_CLIENT_ID,
            'secret': GOOGLE_LOGIN_CLIENT_SECRET
        }
    }
    


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
