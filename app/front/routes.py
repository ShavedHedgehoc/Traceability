from flask import render_template
from flask_login import login_required

from flask import current_app as app
from . import bp
from app import db, celery

from ..tasks import test


@ bp.route('/')
@ bp.route('/index')
@login_required
def index():

    # task = test.apply_async()

    return render_template('index.html', title='Home')
