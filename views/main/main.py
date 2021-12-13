from dash.dependencies import Input, Output
from app import app
from .components_and_modules import layout
from . create_traces import create_traces
from . create_fig import create_fig


@ app.callback(
    Output('main-charts', 'children'),
    [Input('main-years', 'value'),
     Input('main-locations', 'value'),
     Input('main-frequency', 'value'),
     Input('main-chart-sizes', 'value'),
     Input('main-num-suppliers', 'value'),
     Input('main-chart-type', 'value')])
def create_charts(
    years: list[int],
    locations: list[str],
    frequency: str,
    chart_sizes: list[int],
    num_suppliers: int,
    chart_type: str
):
    # temporary fix for some kind of bug.
    # the bug changes the chart_sizes list into a string.
    # this code puts it back into a list.
    if not (isinstance(chart_sizes, list)):
        chart_sizes = [int(x) for x in chart_sizes if x.isdigit()]
        if chart_sizes[0] == 1:
            chart_sizes = [12, 12]

    chart_height_dict = {
        '10': 450, '15': 450, '20': 700, '25': 850,
        '30': 950, '35': 1000, '40': 1100,
        '45': 1200, '50': 1300,
    }

    chart_height = chart_height_dict.get(str(num_suppliers), 550)

    chart_data = create_traces(
        years, locations, frequency, num_suppliers)

    charts = []
    for chart in chart_data:
        fig = create_fig(chart, chart_type, chart_height, chart_sizes)
        charts.append(fig)

    return charts
