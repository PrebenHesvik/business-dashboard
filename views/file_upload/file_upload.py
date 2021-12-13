import base64
import pandas as pd
import numpy as np
import traceback

# dash libs
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State

from plotly_chart_generator import (
    bar_chart,
    chart_styles,
)

from chart_configs import (
    single_color,
    common_layout_args,
    display_chart
)

# dash app
from app import app

# components
from .components_modules import layout

# functions
from functions.clean_data_files import (
    import_and_clean_transactions,
    import_and_clean_supplier_list,
)


def return_errors(error_list: list) -> html.Div:

    error = html.H5('ERROR!', className='msg msg__error')
    msg = html.H5('Excelarket mangler følgende kolonner: ',
                  className='error-message')

    cols_missing = [
        dbc.ListGroupItem(item, className='error-list-item')
        for item in error_list
    ]

    list_group = dbc.ListGroup(
        cols_missing,
        className='error-list',
        horizontal=True
    )

    return html.Div([error, msg, list_group], className='error-div')


def return_success(data: pd.DataFrame | dict, category: str) -> html.Div:
    """
    Returns an html Div with a message and a chart if category is equeal 
    to 'Transaksjoner'. If category is equal to 'Leverandørliste' a
    html.Div with a success message is returned. 
    """
    msg = html.H5('VELLYKKET', className='msg msg__success')

    if category == 'Transaksjoner':
        ser = (
            data
            .drop_duplicates(subset=['Partner', 'Referansenummer'])
            .resample('W', on='Bilagsdato')
            .size()
        )

        ser_df = pd.DataFrame(ser).transpose()

        title = 'Antall faktura lagt til per uke'.upper()

        layout = chart_styles(
            title=title,
            color_palette=single_color,
            **common_layout_args
        )

        traces = bar_chart(ser_df)
        fig = display_chart(traces=traces, layout=layout)
        chart = dcc.Graph(figure=fig)
        return html.Div([msg, chart], className='error-div')
    return html.Div([msg], className='error-div')


def parse_contents(category: str, contents: str, filename: str, date) -> function:
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    ctx = dash.callback_context
    if ctx.triggered[0]['prop_id'] != 'select-data.value':
        try:
            if category == 'Leverandørliste':
                data = import_and_clean_supplier_list(filename, decoded)
                if isinstance(data, list):
                    return return_errors(data)
                np.save('datasets/payment-terms.npy', data)

            elif category == 'Transaksjoner':
                # Returns a DataFrame if file content is
                # is valid, else returns a list of
                # missing columns
                data = import_and_clean_transactions(filename, decoded)
                if isinstance(data, list):
                    return return_errors(data)

                current_data_path = 'datasets/transactions.parquet'
                current_data = pd.read_parquet(current_data_path)

                df = pd.concat([current_data, data], ignore_index=True)
                df.drop_duplicates(inplace=True)
                df = df.set_index('Bilagsdato').sort_index()
                df = df.last('5Y').reset_index()
                df.to_parquet(current_data_path)

        except Exception as e:
            print(e)
            print(traceback.print_exc())
            return html.Div(
                children=[
                    'There was an error processing this file.',
                    html.P(e),
                    html.P(traceback.print_exc()),
                ]
            )

        return return_success(data, category)


@ app.callback(Output('data-response', 'children'),
               [Input('select-data', 'value'),
                Input('upload-data', 'contents')],
               [State('upload-data', 'filename'),
                State('upload-data', 'last_modified')])
def update_output(category: str, list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        return [
            parse_contents(category, c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)
        ]
