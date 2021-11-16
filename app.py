import os
import pathlib
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
from dash import Dash
from flask import Flask
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

# Load dataframes
#from load_datasets import df, payment_terms
