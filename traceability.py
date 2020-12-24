from app import db
from app import create_app, db
from app.models import User


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}


@app.before_first_request
def before_first_request():
    db.create_all(bind='data')


if __name__ == '__main__':
    app.run(host="0.0.0.0")
