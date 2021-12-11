from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash
from dash.html import html
from app import app
import flask_login

import users_mgt as um

from components.dropdown import dropdown
from components import dropdown


def create_user_list_group():
    users = um.show_users()
    list_group_items = [dbc.ListGroupItem(
        x, key=x, n_clicks=0, className="user-item") for x in users]
    return dbc.ListGroup(
        list_group_items, horizontal=True, id='my-own-list-group')


# components/layout for registering new users
email = dbc.FormGroup(
    [
        dbc.Label("Email", width=6),
        dbc.Input(type="email", placeholder="Email", id="register-email"),
    ],
    className="",
)

password = dbc.FormGroup(
    [
        dbc.Label("Password", width=6),
        dbc.Input(type="password", placeholder="Enter password",
                  id="register-pwd"),
    ],
    className="",
)

# submit button for register form
btn_submit = dbc.Button("Legg Til Bruker", id='register-btn', n_clicks=0)

# modules
register_form = dbc.Form(
    [email, password, btn_submit], inline=True, id="register-form",
)

register_title = html.H3('Ny Bruker', className='admin-page-title')

ru1 = dbc.Row(register_title, className='admin-title-row', justify='start')

ru2 = dbc.Row(
    [register_form], id="register-form-container", justify="start")


register_user = html.Div([ru1, ru2], id="user-registration")


def create_user_list(id=None, user=None):
    users = um.show_users()
    try:
        idx = users.index(user)
    except:
        idx = 0

    return dropdown(id=id, value=users[idx], options=users)


user_btn_submit = dbc.Button(
    "Slett Bruker", className="", n_clicks=0,
    id="delete-user-btn", block=False)

# delete users
del_user_title = html.H3('Slett Bruker', className='admin-page-title')
user_list_col = dbc.Col(create_user_list("delete-user"),
                        width=8, id='my-special-col')
del_user_btn = dbc.Col(user_btn_submit, width=4)
ul_r1 = dbc.Row([del_user_title], justify="start", className='admin-title-row')
ul_r2 = dbc.Row([user_list_col, del_user_btn],
                justify="start", id='user-list-row')
ul_div = html.Div([ul_r1, ul_r2], id="remove-user")

# list of all users
users_title = html.H3('Brukere', className='admin-page-title')
users_row_1 = dbc.Row(users_title, justify='start',
                      className='admin-title-row')
users_row_2 = dbc.Row(create_user_list_group(), id='users', justify='start')
users_div = html.Div([users_row_1, users_row_2], id='all-users')


# layout
layout = html.Div([register_user, ul_div, users_div], className='centered')


@app.callback(
    [Output("users", "children"), Output('my-special-col', 'children')],
    [Input("register-btn", "n_clicks"),
     Input("delete-user-btn", "n_clicks"), Input("delete-user", "value")],
    [State("register-email", "value"), State("register-pwd", "value")],
    prevent_initial_call=True)
def admin_action(n_clicks1, n_clicks2, user, email, password):
    current_user = flask_login.current_user
    current_user_email = current_user.email

    admins = [
        'admin@biz.com'
    ]

    ctx = dash.callback_context
    if (
        ctx.triggered[0]['prop_id'] == 'register-btn.n_clicks'
        and email not in um.show_users()
        and '@email.com' in email
        and current_user_email in admins
    ):
        um.add_user(email=email, password=password)
    if (
        ctx.triggered[0]['prop_id'] == 'delete-user-btn.n_clicks'
        and user in um.show_users()
        and current_user_email in admins
    ):
        um.del_user(user)

    user_list = create_user_list(id="delete-user", user=user)
    return create_user_list_group(), user_list
