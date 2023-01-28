from flask import Flask
from os import urandom, path
from flask_sqlalchemy import SQLAlchemy

app_folder = path.dirname(path.abspath(__file__))
app = Flask(__name__, instance_path=app_folder)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/myslifun.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = urandom(24)

db = SQLAlchemy(app)

from . import views
