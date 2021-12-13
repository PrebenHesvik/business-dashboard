from collections import namedtuple
import dash_bootstrap_components as dbc
from dash import dcc

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


def create_fig(
    chart: namedtuple,
    chart_type: str,
    chart_height: str,
    chart_sizes: tuple
) -> dbc.Col:

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
    return dbc.Col([dcc.Graph(figure=fig)], width=chart_sizes[0])
