import click
from flask import Flask
from os import urandom, path
from flask_sqlalchemy import SQLAlchemy


def register_commands():
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create DB after drop')
    def initdb(drop):
        """Initialize database"""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')


app_folder = path.dirname(path.abspath(__file__))
app = Flask(__name__, instance_path=app_folder)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/myslifun.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = urandom(24)

register_commands()

db = SQLAlchemy(app)

from . import views
