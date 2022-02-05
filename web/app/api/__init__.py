from flask import Blueprint

bp = Blueprint('api_bp',
               __name__,
               )
from . import test_models_routes
from . import routes