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

# components
chart_size = dropdown(
    id='main-chart-sizes',
    value=[4, 6],
    options={'Små': [4, 6], 'Medium': [6, 6], 'Store': [12, 12]}
)

num_suppliers = dropdown(
    id='main-num-suppliers',
    value=15,
    options=list(range(10, 55, 5))
)

frequency = dropdown(
    id='main-frequency',
    value='Q',
    options=options['frequency']
)

chart_type = dropdown(
    id='main-chart-type', value='Stolpe',
    options=['Stolpe', 'Linje']
)

year_options = element_options(options=options['year'])
years_checkboxes = radio_check(
    type='check',
    options=year_options,
    value=options['year'],
    id='main-years',
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
    id='main-locations',
    class_name='switch',
    label='Velg Fabrikk',
    with_col=True,
    col_class_name='switch-group'
)

# modules
input_items = [
    list_item('Chart Størrelser', chart_size),
    list_item('Antall Leverandører', num_suppliers),
    list_item('Frekvens', frequency),
    list_item('Graf', chart_type)
]

main_inputs = extended_card(input_items, width=12, xl=12)
switches = dbc.Row([years_checkboxes, factory_checkboxes], justify='center')

# layout
layout = html.Div([main_inputs, switches, dbc.Row(id='main-charts')])
