from flask import Flask
from os import urandom
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/myslifun.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = urandom(24)

db = SQLAlchemy(app)

from . import views
