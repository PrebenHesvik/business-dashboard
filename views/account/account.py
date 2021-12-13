
# dash libs
from dash import dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# From other modules/files
from app import app
from load_datasets import transactions
from functions import filter_dataframe
from .components_modules import (
    acct_dict,
    layout
)
from .functions.aggregations import (
    group_by_location,
    group_by_category,
    group_by_supplier,
    weighted_average_pmt_terms
)
from .functions.create_charts import create_charts


@ app.callback(
    [Output('account_cat_2', 'options'), Output('account_cat_2', 'value')],
    [Input('account_cat_1', 'value')])
def update_account_cat_2(cat_1):
    if cat_1 not in acct_dict:
        return [{'label': '', 'value': ''}], '',

    accts = [{'label': i, 'value': i} for i in acct_dict[cat_1]]
    accts.insert(0, {'label': 'Alle', 'value': 'Alle'})
    return accts, 'Alle'


@ app.callback(
    [Output('account_cat_3', 'options'), Output('account_cat_3', 'value')],
    [Input('account_cat_1', 'value'),
     Input('account_cat_2', 'value')])
def update_account_cat_3(cat_1, cat_2):
    if not any([cat_2 == 'Alle', len(cat_2) == 0]):
        acc = [{'label': i, 'value': i} for i in acct_dict[cat_1][cat_2]]
        acc.insert(0, {'label': 'Alle', 'value': 'Alle'})
        return acc, 'Alle'
    else:
        return [{'label': '', 'value': ''}], ''


@ app.callback(
    [Output('account_cat_4', 'options'), Output('account_cat_4', 'value')],
    [Input('account_cat_1', 'value'),
     Input('account_cat_2', 'value'),
     Input('account_cat_3', 'value')])
def update_account_cat_4(cat_1, cat_2, cat_3):
    if not any([cat_3 == 'Alle', len(cat_3) == 0]):
        if isinstance(acct_dict[cat_1][cat_2][cat_3], dict):
            acc = [{'label': i, 'value': i}
                   for i in acct_dict[cat_1][cat_2][cat_3]]
            acc.insert(0, {'label': 'Alle', 'value': 'Alle'})
            return acc, 'Alle'
        else:
            return [{'label': '-', 'value': ''}], ''
    else:
        return [{'label': '-', 'value': ''}], ''


@ app.callback(
    Output('account-main-chart', 'children'),
    [Input('account-years', 'value'),
     Input('account-locations', 'value'),
     Input('account-show', 'value'),
     Input('account-frequency', 'value'),
     Input('account_cat_1', 'value'),
     Input('account_cat_2', 'value'),
     Input('account_cat_3', 'value'),
     Input('account_cat_4', 'value')])
def main_chart(years, locations, show, frequency,
               cat_1, cat_2, cat_3, cat_4):
    """
    """

    # filter dataframe
    df = filter_dataframe(transactions, years, locations, frequency)

    # account category dict
    categories = [cat_1, cat_2, cat_3, cat_4]

    # set title on charts group_by_loc and group_by_cat
    cats = [cat for cat in categories if cat != '']
    if 'Alle' in cats:
        string = cats[cats.index('Alle') - 1]
        string = '' if string == 'Alle' else string + ' -'
    else:
        string = cats[-1]
    title = f'{string} {show}'
    substr_title = title.split("/")[0]

    df_group_by_loc = group_by_location(df, show, frequency, categories)
    data_group_by_cat = group_by_category(df, show, frequency, categories)
    df_group_by_sup = group_by_supplier(df, show, frequency, categories)
    df_wa_pmt_terms = weighted_average_pmt_terms(
        df, frequency, categories, data_group_by_cat)

    chart_data = [
        (df_group_by_loc, f'{title} - gruppert etter fabrikk'),
        (data_group_by_cat, f'{title} - gruppert etter kategori'),
        (df_group_by_sup, f'{substr_title} - gruppert etter leverandør'),
        (df_wa_pmt_terms, 'Vektede betalingsbetingelser - gruppert etter kategori'),
    ]

    return create_charts(chart_data)
