from flask import Flask
from flask_pony import Pony


app = Flask(__name__)
app.config.from_object('config.Config')

from app.models import db

db.bind(**app.config['PONY'])
db.generate_mapping(create_tables=True)

Pony(app)

from app import views
