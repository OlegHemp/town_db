import os
class Configuration(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///myapp.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'MY_Secret_Key'
    DEBUG = True
