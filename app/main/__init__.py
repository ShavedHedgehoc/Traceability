from flask import Blueprint

bp = Blueprint('main_bp',
                __name__,
                template_folder='templates'                
    )

from . import routes