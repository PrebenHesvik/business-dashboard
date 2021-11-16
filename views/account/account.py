# dash libs
from dash import dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from flatten_dict import flatten

from app import app

from plotly_chart_generator import (
    bar_chart,
    line_chart,
    chart_styles,
)

from chart_configs import (
    single_color,
    multi_color,
    common_layout_args,
    display_chart
)

from load_datasets import transactions

from functions import filter_dataframe

from .components_modules import (
    acct_dict,
    account_categories,
    show,
    frequency,
    years_checkboxes,
    factory_checkboxes,
    layout
)

from .functions import (
    groupby,
    pivot,
    supplier_pmt_terms,
    transpose_sort_delete,
    wa_pmt_terms,
)
#from . aggregations import create_traces


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
    """[summary]

    :param years:
        list of years - used to filter df
    :type years:
        list
    :param locations:
        list of locations - used to filter df
    :type locations:
        list
    :param show:
        [description]
    :type show:
        str
    :param
        frequency: [description]
    :type
        frequency: str
    :return:
        [description]
    :rtype:
        [type]
    """

    # print(locals())

    # filter dataframe
    fd = filter_dataframe(transactions, years, locations, frequency)

    if not any([cat_4 == '', cat_4 == 'Alle']):
        accounts = acct_dict[cat_1][cat_2][cat_3][cat_4]

        # group data by location
        df_group_by_loc = pivot(
            fd, accounts, show, frequency, 'Lokasjon')

    elif not any([cat_3 == '', cat_3 == 'Alle']):
        accounts = acct_dict[cat_1][cat_2][cat_3]

        if not isinstance(accounts, int):
            account_list = flatten(accounts).values()

            # data for chart group_by_loc
            df_group_by_loc = pivot(
                fd, account_list, show, frequency, 'Lokasjon')

        else:
            # data for chart group_by_loc
            df_group_by_loc = pivot(
                fd, accounts, show, frequency, 'Lokasjon')

    elif not any([cat_2 == '', cat_2 == 'Alle']):
        d = acct_dict[cat_1][cat_2]

        # data for chart grpby_loc
        accounts = flatten(d).values()
        df_group_by_loc = pivot(
            fd, accounts, show, frequency, 'Lokasjon')

    elif cat_2 == 'Alle':
        d = acct_dict[cat_1]

        # data for chart grpby_loc
        accounts = flatten(d).values()
        df_group_by_loc = pivot(
            fd, accounts, show, frequency, 'Lokasjon')

    elif cat_1 == 'Alle':
        # data for chart group_by_loc
        accounts = flatten(acct_dict).values()
        df_group_by_loc = pivot(
            fd, accounts, show, frequency, 'Lokasjon')

    # chart layouts

    # set title on charts group_by_loc and group_by_cat
    cats = [cat for cat in [cat_1, cat_2, cat_3, cat_4] if cat != '']

    if 'Alle' in cats:
        string = cats[cats.index('Alle') - 1]
        string = '' if string == 'Alle' else string + ' -'
    else:
        string = cats[-1]

    title = f'{string} {show}'
    substr_title = title.split("/")[0]

    chart_data = [
        (df_group_by_loc, f'{title} - gruppert etter fabrikk'),
    ]

    charts = []
    for frame, title in chart_data:
        cp = multi_color if frame.index.size > 1 else single_color

        layout = chart_styles(
            title=title.upper(),
            color_palette=cp,
            **common_layout_args
        )

        trace = bar_chart(df=frame)

        fig = display_chart(traces=trace, layout=layout)

        chart_obj = dbc.Col([dcc.Graph(figure=fig)], width=12)

        charts.append(chart_obj)

    return charts
