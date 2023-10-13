from flask import Flask
from flask_login import LoginManager
from pony.flask import Pony


app = Flask(__name__)
app.config.from_object('config.Config')

from app.models import db

db.bind(**app.config['PONY'])
db.generate_mapping(create_tables=True)

Pony(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return db.User.get(id=user_id)


from app import views