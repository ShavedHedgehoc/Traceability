from flask import Blueprint

bp = Blueprint('front_bp',
               __name__,
               template_folder='templates'
               )

from . import routes
