from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from config import Config

db = SQLAlchemy()


def create_app():

    app = Flask(__name__)

    app.config.from_object("config.Config")
    db.init_app(app)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp)

    from app.front import bp as front_bp
    app.register_blueprint(front_bp)
    
    return app
