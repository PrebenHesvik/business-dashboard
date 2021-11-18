import dash_bootstrap_components as dbc
from dash import html
from collections import namedtuple

# use the Row and Col components to construct the sidebar header
# it consists of a title, and a toggle, the latter is hidden on large screens
sidebar_header = dbc.Row(
    [
        dbc.Col(dbc.NavLink(
            html.H5("BIZ", className="display-4"),
            href="/login",
        )),
        dbc.Col(
            html.Button(
                # use the Bootstrap navbar-toggler classes to style the toggle
                html.Span(className="fas fa-bars navbar-toggler-icon"),
                # the navbar-toggler classes don't set color, so we do it here
                style={"color": "rgba(0,0,0,.5)",
                       "borderColor": "rgba(0,0,0,.1)", },
                id="toggle",
            ),
            # the column containing the toggle will be only as wide as the
            # toggle, resulting in the toggle being right aligned
            width="auto",
            # vertically align the toggle in the center
            align="center",
        ),
    ],
    justify="center",
    # no_gutters=True,
)

NavLink = namedtuple('NavLink', 'class_name href id')

nav_links = [
    NavLink('fas fa-money-check-alt', '/page-1', 'page-1-link'),
    NavLink('fas fa-coins', '/page-2', 'page-2-link'),
    NavLink('fas fa-building', '/page-3', 'page-3-link'),
    NavLink('fas fa-file-upload', '/page-4', 'page-4-link'),
    NavLink('fas fa-users', '/page-5', 'page-5-link'),
    NavLink('fas fa-arrow-circle-left', '/page-6', 'page-6-link'),
]

# Create a react NavLink component for each namedtuple in nav_links
# and store all the NavLinks in a list
dbc_nav_links = []
for nav_link in nav_links:
    dbc_nl = dbc.NavLink(
        children=html.I(className=nav_link.class_name),
        href=nav_link.href,
        id=nav_link.id)
    dbc_nav_links.append(dbc_nl)

# complete sidebar module
sidebar = html.Div(
    [
        sidebar_header,
        # wrap the horizontal rule and short blurb in a div that can be
        # hidden on a small screen
        html.Div([html.Hr(className="sep-line"), ], id="blurb",),
        # use the Collapse component to animate hiding / revealing links
        dbc.Collapse(
            dbc.Nav(
                dbc_nav_links,
                vertical=True,
                pills=False,
            ),
            id="collapse",
        ),
    ],
    id="sidebar",
)
