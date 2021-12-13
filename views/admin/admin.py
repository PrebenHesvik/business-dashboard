from dash.dependencies import Input, Output, State
import dash
from app import app
import flask_login

import users_mgt as um
from config import settings

from .components_modules import (
    layout,
    create_user_list,
    create_user_list_group
)


@app.callback(
    [Output("users", "children"), Output('user-list-col', 'children')],
    [Input("register-btn", "n_clicks"),
     Input("delete-user-btn", "n_clicks"), Input("delete-user", "value")],
    [State("register-email", "value"), State("register-pwd", "value")],
    prevent_initial_call=True)
def admin_action(n_clicks1, n_clicks2, user, email, password):
    current_user = flask_login.current_user

    admins = [
        settings.admin
    ]

    ctx = dash.callback_context
    if (
        ctx.triggered[0]['prop_id'] == 'register-btn.n_clicks'
        and email not in um.show_users()
        and '@email.com' in email
        and current_user.email in admins
    ):
        um.add_user(email=email, password=password)
    if (
        ctx.triggered[0]['prop_id'] == 'delete-user-btn.n_clicks'
        and user in um.show_users()
        and user not in admins
        and current_user.email in admins
    ):
        um.del_user(user)

    user_list = create_user_list(id="delete-user", user=user)
    return create_user_list_group(), user_list
