import os
import pathlib
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
from dash import Dash
from flask import Flask
from sqlalchemy.engine.reflection import Inspector
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from config import settings


server = Flask(__name__)
app = Dash()

app = Dash(
    __name__,
    server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{"name": "viewport",
                "content": "width=device-width, initial-scale=1"}],
    external_scripts=["https://kit.fontawesome.com/50d678538c.js"],
    suppress_callback_exceptions=True,
)

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

app.server.config.update(
    SECRET_KEY=settings.secret_key,
    SQLALCHEMY_DATABASE_URI=settings.sqlalchemy_database_uri,
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

# set up database
db = SQLAlchemy(app.server)
db.init_app(app.server)
engine = create_engine(settings.sqlalchemy_database_uri)


inspector = Inspector.from_engine(engine)
if not inspector.get_table_names():
    from users_mgt import create_user_table
    create_user_table()
    print('New usertable has been created.')

inspector = Inspector.from_engine(engine)
if 'user' in inspector.get_table_names():
    from users_mgt import show_users
    users = show_users()
    print(users, inspector.get_table_names())
    if settings.admin not in users:
        from users_mgt import add_user
        add_user(settings.admin, settings.admin_password)
        print('admin has been created')

# Setup the LoginManager for the server
login_manager = LoginManager()
login_manager.init_app(app.server)
login_manager.login_view = "/login"
from users_mgt import User as base


class User(UserMixin, base):
    """Create User class with UserMixin"""
    pass


print('We are still ok')


login_manager.user_loader


def load_user(user_id):
    return User.query.get(int(user_id))
