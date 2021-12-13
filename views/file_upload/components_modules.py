import dash_bootstrap_components as dbc
from dash import html, dcc

# Import components
from components import (
    element_options,
    radio_check,
)

# components
header = html.H1('Last opp CSV eller XLS', className='upload-header')

# Files available for user upload
files = [
    'Transaksjoner',
    'Leverandørliste'
]

file_options = element_options(files)
select_file = radio_check(
    type='radio',
    options=file_options,
    value='Transaksjoner',
    id='select-data',
    class_name='switch',
    label=None,
    with_col=False,
    col_class_name='switch-group',
    col_width=4,
    col_width_xl=3
)


upload = dcc.Upload(
    id='upload-data',
    children=html.Div(
        ['Dra og Slipp eller ', html.A('Velg Fil', className='green')]),
    # Allow multiple files to be uploaded
    multiple=True
)

response = html.Div(dcc.Loading(
    id="loading-spinner",
    children=[html.Div(id='data-response')],
    type="circle"),
    id='data-response-container')

modules = [
    dbc.Row(
        children=[header, select_file, upload, response],
        id='upload-data-div'),
]

layout = html.Div(modules, className='upload-container')
