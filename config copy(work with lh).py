import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    JSON_AS_ASCII = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    # CELERY_BROKER_URL = 'redis://redis:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    # CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
    # RESULT_BACKEND = 'redis://redis:6379/0'
    RESULT_BACKEND = 'redis://localhost:6379/0'
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}/{}'.format(
        os.environ.get('POSTGRES_USER'),
        os.environ.get('POSTGRES_PASSWORD'),
        os.environ.get('POSTGRES_HOST'),
        os.environ.get('POSTGRES_DB')
    )

    SQLALCHEMY_BINDS = {
        'data': os.environ.get('DB_URI2')
    }

class DevConfig(Config):
    LOGLEVEL = "DEBUG"
    DEVELOPMENT = True
    DEBUG = True
    TESTING = False
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SESSION_COOKIE_NAME = 'SESSION_COOKIE_NAME'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}/{}'.format(
    #     os.environ.get('POSTGRES_USER'), 
    #     os.environ.get('POSTGRES_PASSWORD'),
    #     os.environ.get('POSTGRES_HOST'),
    #     os.environ.get('POSTGRES_DB')          
    #     )
    
    # SQLALCHEMY_BINDS = {
    #     'data': os.environ.get('DB_URI2')
    # }


class TestConfig(Config):
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    DEBUG = True
    TESTING = True
    CSRF_ENABLED = True
    SECRET_KEY = 'SECRET_KEY'
    SESSION_COOKIE_NAME = 'SESSION_COOKIE_NAME'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI')
    # SQLALCHEMY_BINDS = {
    #     'data': os.environ.get('DB_URI2')
    # }

class ProdConfig(Config):
    LOGLEVEL = "DEBUG"
    DEVELOPMENT = True
    DEBUG = True
    TESTING = False
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SESSION_COOKIE_NAME = 'SESSION_COOKIE_NAME'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI')
    # SQLALCHEMY_BINDS = {
    #     'data': os.environ.get('DB_URI2')
    # }
