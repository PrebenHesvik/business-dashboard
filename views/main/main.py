# dash libs
from dash import dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app

from plotly_chart_generator import (
    bar_chart,
    line_chart,
    chart_styles,
)

from chart_configs import (
    single_color,
    common_layout_args,
    display_chart
)

from .components_and_modules import *
from . create_traces import create_traces


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

        layout = chart_styles(
            color_palette=single_color,
            title=chart.title.upper(),
            **common_layout_args
        )

        if chart_type == 'Linje' and chart.chart_type == 'both':
            max_yaxis = chart.data.max().max() * 1.3
            min_yaxis = chart.data.min().min() * 0
            yaxis_range = [min_yaxis, max_yaxis]

            layout['yaxis_autorange'] = False
            layout['yaxis_range'] = yaxis_range

            traces = line_chart(
                chart.data,
                line_smoothing=1,
                marker_size=10,
                mode='lines+markers'
            )
        else:
            if chart.dynamic_height is True:
                layout['height'] = chart_height
                layout['yaxis_showgrid'] = False
                layout['xaxis_showgrid'] = True

            if chart.chart_type == 'bar':
                traces = bar_chart(df=chart.data, orientation='h')
            else:
                traces = bar_chart(df=chart.data)

        fig = display_chart(traces=traces, layout=layout)
        fig_col = dbc.Col([dcc.Graph(figure=fig)], width=chart_sizes[0])
        charts.append(fig_col)

    return charts
