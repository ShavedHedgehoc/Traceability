import pyodbc
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from datetime import timedelta
from celery import Celery

db = SQLAlchemy()

celery = Celery(__name__, broker=Config.CELERY_BROKER_URL,
                include=['app.tasks'])
celery.config_from_object('celeryconfig')

login = LoginManager()
login.login_view = 'auth_bp.login'


def create_app():

    app = Flask(__name__)

    if app.config["ENV"] == "development":
        app.config.from_object("config.DevConfig")
    elif app.config["ENV"] == "testing":
        app.config.from_object("config.TestConfig")
    elif app.config["ENV"] == "production":
        app.config.from_object("config.ProdConfig")

    from .models import User, Author

    db.init_app(app)

    migrate = Migrate(app, db)
    login.init_app(app)

    celery.conf.update(app.config)

    from app.front import bp as front_bp
    app.register_blueprint(front_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)   

    return app
