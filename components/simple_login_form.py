from dash import html, dcc
import dash_bootstrap_components as dbc


def simple_login_form(form_title, use_labels=False):
    title = html.H1(form_title, className="login-title")
    username = dbc.Input(type="email", placeholder="Email", id="email-input")
    password = dbc.Input(
        type="password", placeholder="Enter password", id="password-input")

    if use_labels is not False:
        username_label = dbc.Label(
            "Email", className="form-label", color="white", width=6)
        password_label = dbc.Label(
            "Password", className="form-label", color="white", width=6)
    else:
        username_label, password_label = None, None

    email = html.Div([username_label, username], className="form-group")
    password = html.Div([password_label, password], className="form-group")

    btn_submit = dbc.Button("Logg inn", n_clicks=0, id="login-btn")
    button = html.Div([btn_submit], className="d-grid gap-2")

    msg_field = html.Div(children="", id="output-state")

    login_form = dbc.Form(
        [title, email, password, button, msg_field], id="login-form")
    return dbc.Row([login_form], id="login-form-container")
