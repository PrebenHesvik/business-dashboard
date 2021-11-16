import dash_bootstrap_components as dbc
from dash import dcc
from .element_options import element_options


def dropdown(
    d_type="dbc",
    id="",
    value="",
    options=None,
    class_name=None,
    multi=False,
    placeholder=None,
):

    if options is not None:
        options = element_options(options)

    if d_type == "dbc":
        return dbc.Select(
            id=id,
            value=value,
            className=class_name,
            options=options
        )
    else:
        return dcc.Dropdown(
            options=options,
            multi=multi,
            className=class_name,
            placeholder=placeholder,
            id=id,
            value=value,
        )
