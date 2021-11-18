import dash_bootstrap_components as dbc
from dash import html

# Import components
from components import (
    dropdown,
    element_options,
    extended_card,
    radio_check,
    list_item
)

from load_datasets import options

from load_datasets import transactions

# components
suppliers_list = (
    transactions.Partner
    .dropna()
    .sort_values()
    .unique()
    .tolist()
)

supplier_dropdown = dropdown(
    d_type='dcc',
    id='supplier-dropdown',
    value='NO28432',
    options=suppliers_list
)

frequency = dropdown(
    id='supplier-frequency',
    value='Q',
    options=options['frequency']
)

size_options = {'Medium': [6, 12], 'Store': [12, 12]}
chart_sizes = dropdown(
    id='supplier-chart-size',
    value=[6, 12],
    options=size_options
)

year_options = element_options(options=options['year'])
years_checkboxes = radio_check(
    type='check',
    options=year_options,
    value=options['year'],
    id='supplier-years',
    class_name='switch',
    label='Velg År',
    with_col=True,
    col_class_name='switch-group',
    col_width=6,
    col_width_xl=4
)

factory_options = element_options(options['factory'])
factory_checkboxes = radio_check(
    type='check',
    options=factory_options,
    value=options['factory'],
    id='supplier-locations',
    class_name='switch',
    label='Velg Fabrikk',
    with_col=True,
    col_class_name='switch-group'
)

# modules
input_items = [
    list_item('Leverandør', supplier_dropdown, class_name='flex-grow-2'),
    list_item('Frekvens', frequency),
    list_item('Graf størrelser', chart_sizes)]

inputs = extended_card(input_items, width=12, xl=12)
switches = dbc.Row([years_checkboxes, factory_checkboxes], justify='center')

# layout
layout = html.Div(children=[inputs, switches, dbc.Row(id='supplier-charts')])