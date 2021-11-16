import dash_bootstrap_components as dbc
from dash import html


def extended_card(items, width, **kwargs):
    children = [dbc.ListGroup(items, horizontal='sm')]
    return dbc.Row(
        dbc.Col(
            children,
            className='extended-cards',
            width=width,
            **kwargs),
        className='extended-cards-row')


def list_item(heading, item, class_name=None):
    return dbc.ListGroupItem(
        [
            html.H5(heading, className='list-group-item-heading'),
            item
        ],
        className=class_name)
