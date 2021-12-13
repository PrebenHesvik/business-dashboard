from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import datetime as dt
from app import app, User

from flask_login import login_user, confirm_login
from werkzeug.security import check_password_hash

#from .components_modules import layout
from components.simple_login_form import simple_login_form


# layout
login_form = simple_login_form('Velkommen til Business Dashboard')
layout = html.Div([dcc.Location(id="url_login", refresh=True), login_form])


@app.callback(
    Output("url_login", "pathname"),
    [Input("login-btn", "n_clicks")],
    [State("email-input", "value"), State("password-input", "value")],
)
def login(n_clicks, email, password):
    """Logs user into the site"""
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        return "/page-1"


@app.callback(
    Output("output-state", "children"),
    [Input("login-btn", "n_clicks")],
    [State("email-input", "value"), State("password-input", "value")],
)
def login_message(n_clicks, email, password):
    """Displays a message if the login credentials are wrong"""
    if n_clicks <= 0:
        return ""
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        return ""
    else:
        return html.P(
            "Incorrect username or password", style={"color": "white"}
        )
