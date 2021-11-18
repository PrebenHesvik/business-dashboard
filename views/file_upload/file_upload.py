import base64
import pandas as pd
import numpy as np
import datetime as dt
import io
import traceback
from calendar import monthrange
import pathlib

# dash libs
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from plotly_chart_generator import (
    bar_chart,
    line_chart,
    chart_styles,
)

from chart_configs import (
    single_color,
    highlight_color,
    multi_color,
    common_layout_args,
    display_chart
)

# dash app
from app import  app

# components
from components.element_options import element_options
from components.radio_check import radio_check
from dash.dependencies import Input, Output, State

# functions
from functions.clean_data_files import (
    clean_transactions,
    import_contracts,
    import_supplier_list,
    inetto_production
)

from .components_modules import layout


def return_errors(error_list):

    error = html.H5('ERROR!', className='msg msg__error')
    msg = html.H5('Excelarket mangler følgende kolonner: ',
                  className='error-message')

    list_items = [dbc.ListGroupItem(
        item, className='error-list-item') for item in error_list]
    list_group = dbc.ListGroup(
        list_items, className='error-list', horizontal=True)
    return html.Div([error, msg, list_group], className='error-div')


def return_success(data, category):
    msg = html.H5('VELLYKKET', className='msg msg__success')
    if category == 'Transaksjoner':
        ser = (data
               .drop_duplicates(subset=['Partner', 'Referansenummer'])
               .resample('W', on='Bilagsdato')
               .size())

        ser_df = pd.DataFrame(ser).transpose()

        title = 'Antall faktura lagt til per uke'.upper()

        layout = chart_styles(
            title=title, color_palette=single_color,
            showlegend=False, **common_layout_args)
        traces = bar_chart(ser_df)
        fig = display_chart(traces=traces, layout=layout)
        chart = dcc.Graph(figure=fig)
        return html.Div([msg, chart], className='error-div')

    elif category in ['Kontrakter', 'Leverandørliste', 'iNetto produksjonsdata']:
        return html.Div([msg], className='error-div')


PATH = pathlib.Path(__file__).parent
#DATA_PATH = PATH.joinpath("datasets").resolve()
#DF = pd.read_parquet(DATA_PATH.joinpath("transactions.parquet"))


def parse_contents(category, contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    ctx = dash.callback_context
    if ctx.triggered[0]['prop_id'] != 'select-data.value':
        try:
            if category == 'Transaksjoner':
                data = clean_transactions(filename, decoded)
                if isinstance(data, list):
                    return return_errors(data)

                current_data_path = 'datasets/transactions.parquet'
                current_data = pd.read_parquet(current_data_path)

                df = pd.concat([current_data, data], ignore_index=True)
                df.drop_duplicates(inplace=True)
                df = df.set_index('Bilagsdato').sort_index()
                df = df.last('5Y').reset_index()
                df.to_parquet(current_data_path)

            elif category == 'Kontrakter':
                data = import_contracts(filename, decoded)
                if isinstance(data, list):
                    return return_errors(data)
                data.to_parquet('data/contracts.parquet')

            elif category == 'Leverandørliste':
                data = import_supplier_list(filename, decoded)
                if isinstance(data, list):
                    return return_errors(data)
                else:
                    np.save('datasets/payment-terms.npy', data)

            else:
                data = inetto_production(filename, decoded)
                if isinstance(data, list):
                    return return_errors(data)
                else:
                    writer = pd.ExcelWriter('datasets/inetto_production.xlsx')
                    data.to_excel(writer, index=True)

        except Exception as e:
            print(e)
            print(traceback.print_exc())
            return html.Div([
                'There was an error processing this file.',
                html.P(e), html.P(traceback.print_exc())
            ])

        return return_success(data, category)


@ app.callback(Output('data-response', 'children'),
               [Input('select-data', 'value'),
                Input('upload-data', 'contents')],
               [State('upload-data', 'filename'),
                State('upload-data', 'last_modified')])
def update_output(category, list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:

        children = [
            parse_contents(category, c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]

        return children