"""Renders page content"""
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from app import app
from config import settings

# Import each individual page
from views import (
    main,
    file_upload,
    account,
    supplier,
    # production,
    # login,
    # admin
)

# Import components
from components.sidebar import sidebar

# Page layout
content = html.Div(id="page-content")
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), sidebar, content])

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
        return True, False, False, False, False, False, False
    return [pathname == f"/page-{i}" for i in range(1, 7)]


# def authenticated(layout):
#     """Returns the layout if user is authenticated"""
#     if not current_user.is_authenticated:
#         return login_manager.unauthorized()
#     else:
#         return layout


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    """Renders page content according to the link the user clicks"""
    match pathname:
        case "/" | "/login" | "/page-1":
            return main.layout
        case "/page-2":
            return account.layout
        case "/page-3":
            return supplier.layout
        case "/page-4":
            return file_upload.layout

    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
    app.run_server(debug=settings.debug)
