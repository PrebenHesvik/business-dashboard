from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import datetime as dt
from app import app, User

from flask_login import login_user, confirm_login
from werkzeug.security import check_password_hash

# components
title = html.H1("Velkommen til Business Dashboard", className="login-title")

email = html.Div(
    [
        #dbc.Label("Email", className="form-label", color="white", width=6),
        dbc.Input(type="email", placeholder="Email", id="email-box"),
    ],
    className="form-group-new",
)

password = html.Div(
    [
        #dbc.Label("Password", className="form-label", color="white", width=6),
        dbc.Input(type="password", placeholder="Enter password", id="pwd-box"),
    ],
    className="form-group-new",
)

btn_submit = dbc.Button(
    "Logg inn", className="form-button", n_clicks=0,
    id="login-button",
)
button = html.Div(
    [
        btn_submit
    ],
    className="d-grid gap-2",
)

msg_field = html.Div(children="", id="output-state")

# modules
login_form = dbc.Form(
    [title, email, password, button, msg_field],
    id="login-form",
)

login_form_row = dbc.Row([login_form], id="login-form-container")

# layout
layout = html.Div([dcc.Location(id="url_login", refresh=True), login_form_row])

print(type(User))
print(User)
User.query.filter_by(email='admin').first()


@app.callback(
    Output("url_login", "pathname"),
    [Input("login-button", "n_clicks")],
    [State("email-box", "value"), State("pwd-box", "value")],
)
def login(n_clicks, email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        return "/page-1"


@app.callback(
    Output("output-state", "children"),
    [Input("login-button", "n_clicks")],
    [State("email-box", "value"), State("pwd-box", "value")],
)
def login_message(n_clicks, email, password):
    """
    Gives a message to the user if the login credentials
    typed in is wrong.

    Parameters
    ----------
    n_clicks : [type]
        [description]
    email : [type]
        [description]
    password : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """
    if n_clicks <= 0:
        return ""
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        return ""
    else:
        return html.P(
            "Incorrect username or password", style={"color": "white"}
        )
