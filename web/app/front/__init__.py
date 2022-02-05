from flask import Blueprint

bp = Blueprint('front_bp',
               __name__,
               )
from . import routes