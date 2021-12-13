import dash_bootstrap_components as dbc
from dash import html

from components import dropdown
import users_mgt as um


def add_user_form():
    email = dbc.Input(
        type="email",
        placeholder="Email",
        id="register-email"
    )
    password = dbc.Input(
        type="password",
        placeholder="Enter password",
        id="register-pwd"
    )
    btn = dbc.Button(
        "Legg Til Bruker",
        id='register-btn',
        n_clicks=0
    )
    email_col = dbc.Col(
        [email],
        className="form__inline--form-group",
        width=4,
    )
    password_col = dbc.Col(
        [password],
        className="form__inline--form-group",
        width=4,
    )
    btn_col = dbc.Col(
        btn,
        width=4,
        className=""
    )
    return dbc.Row(
        dbc.Form(
            [email_col, password_col, btn_col],
        ),
        className='gx-1'
    )


# components/modules for registering new users
register_title = html.H3(
    'Ny Bruker',
    className='admin-page-title'
)

row_1 = dbc.Row(
    register_title,
    className='admin-title-row',
    justify='start'
)

row_2 = dbc.Row(
    [add_user_form()],
    id="register-form-container",
    justify='start'
)

register_user = html.Div(
    [row_1, row_2],
    id="user-registration"
)

# Functions, components and modules
# for removing a user


def create_user_list_group():
    list_group_items = [
        dbc.ListGroupItem(
            children=user,
            key=user,
            n_clicks=0,
            className="user-item"
        )
        for user in um.show_users()
    ]
    return dbc.ListGroup(
        list_group_items,
        horizontal=True,
        id='my-own-list-group'
    )


def create_user_list(id=None, user=None):
    users = um.show_users()
    idx = 0 if user is None else users.index(user)
    return dropdown(id=id, value=users[idx], options=users)


del_user_title = html.H3('Slett Bruker', className='admin-page-title')

user_list_col = dbc.Col(
    create_user_list("delete-user"),
    width=8,
    id='user-list-col')

user_btn_submit = dbc.Button(
    "Slett Bruker",
    className="",
    n_clicks=0,
    id="delete-user-btn"
)

del_user_btn = dbc.Col(user_btn_submit, width=4)

dl_row_1 = dbc.Row(
    [del_user_title],
    justify="start",
    className='admin-title-row'
)

dl_row_2 = dbc.Row(
    [user_list_col, del_user_btn],
    justify="start",
    id='user-list-row'
)


delete_user = html.Div(
    [dl_row_1, dl_row_2],
    id="remove-user"
)


# Display list of all users
users_title = html.H3('Brukere', className='admin-page-title')

row_users_title = dbc.Row(
    users_title,
    justify='start',
    className='admin-title-row'
)

row_users_list = dbc.Row(
    create_user_list_group(),
    id='users',
    justify='start'
)

users_div = html.Div(
    [row_users_title, row_users_list],
    id='all-users'
)

# Final layout
layout = html.Div(
    [register_user, delete_user, users_div],
    className='centered'
)
