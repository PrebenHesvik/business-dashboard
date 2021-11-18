from .supplier_comparison_charts import supplier_comparison_charts
from collections import namedtuple
from dash.dependencies import Input, Output

from app import app

from functions import filter_dataframe

from load_datasets import transactions

from .components_modules import layout
from .create_chart import create_chart
from.create_chart_data import (
    supplier_spend_data,
    supplier_invoices_data,
    spend_grouped_by_location,
    invoice_grouped_by_location,
    spend_grouped_by_account,
    num_invoices_grouped_by_account,
)


@ app.callback(
    Output('supplier-charts', 'children'),
    [Input('supplier-dropdown', 'value'),
     Input('supplier-years', 'value'),
     Input('supplier-locations', 'value'),
     Input('supplier-frequency', 'value'),
     Input('supplier-chart-size', 'value'), ])
def charts(supplier, years, locations, frequency, chart_size):

    # temporary fix for some kind of bug.
    # the bug changes the chart_sizes list into a string.
    # this code puts it back into a list.
    if not (isinstance(chart_size, list)):
        chart_size = [6, 12] if chart_size.startswith('6') else [12, 12]

    attrs = 'data title chart_type marker_colors orientation width'
    ChartData = namedtuple('ChartInfo', attrs)

    chart_data_list = []
    if supplier is not None:
        part_filt_df = filter_dataframe(
            transactions, years, locations, frequency)
        filter_1 = part_filt_df['Partner'] == supplier
        df = part_filt_df.loc[filter_1]

        chart_data_list = [
            supplier_spend_data(df, frequency, chart_size, ChartData),
            supplier_invoices_data(df, frequency, chart_size, ChartData),
            spend_grouped_by_location(df, frequency, chart_size, ChartData),
            invoice_grouped_by_location(df, frequency, chart_size, ChartData),
            spend_grouped_by_account(df, frequency, chart_size, ChartData),
            num_invoices_grouped_by_account(
                df, frequency, chart_size, ChartData),
        ]

        spend_acct_sorted = spend_grouped_by_account(
            df, frequency, chart_size, ChartData, return_just_pivot=True)
        accounts = spend_acct_sorted.columns.tolist()
        comparison_charts = supplier_comparison_charts(
            part_filt_df, accounts, supplier, chart_size, ChartData)

        chart_data_list.extend(comparison_charts)

        return create_chart(chart_data_list)
