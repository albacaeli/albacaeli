"""
Alba Caeli
A webapp to log deep sky observations, socially.
"""

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.creole import Creole

from config import basedir

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = "login"

creole = Creole(app)


from app import views, models, forms
