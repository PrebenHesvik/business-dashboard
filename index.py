"""Renders page content"""
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from config import settings
from flask_login import logout_user, current_user

from app import app, login_manager

# Import each individual page
from views import (
    main,
    file_upload,
    account,
    supplier,
    login,
    admin
)

# Import components
from components.sidebar import sidebar

# Page layout
app.layout = html.Div(
    children=[
        dcc.Location(id="url", refresh=False),
        sidebar,
        html.Div(id="page-content")
    ]
)

# Callbacks


@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 7)],
    [Input("url", "pathname")])
def toggle_active_links(pathname):
    """
    Uses the current pathname to set the active state of the corresponding
    nav link to true, allowing users to tell what page they are on.
    """
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False, False, False, False
    return [pathname == f"/page-{i}" for i in range(1, 7)]


def authenticated(layout):
    """Returns the layout if user is authenticated"""
    if current_user.is_authenticated:
        return layout
    logout_user()
    return login.layout


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    """Renders page content according to the link the user clicks"""
    match pathname:
        case '/' | '/login':
            return login.layout
        case '/page-1':
            return authenticated(main.layout)
        case '/page-2':
            return authenticated(account.layout)
        case '/page-3':
            return authenticated(supplier.layout)
        case '/page-4':
            return authenticated(file_upload.layout)
        case '/page-5':
            return authenticated(admin.layout)
        case '/page-6':
            if current_user.is_authenticated:
                logout_user()
            return login.layout

    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        dbc.Container(
            [
                html.H1("404: Not found", className="text-danger"),
            ],
            fluid=True,
            className="py-3",
        ),
        className="p-3 bg-dark rounded-3",
    )


if __name__ == "__main__":
    app.run_server(debug=settings.debug)
