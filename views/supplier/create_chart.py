import dash_bootstrap_components as dbc
from dash import dcc

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

def create_chart(chart_data_list):
    charts = []
    for info in chart_data_list:
        if info.orientation == 'h':
            xaxis_grid, yaxis_grid = True, False
        else:
            xaxis_grid, yaxis_grid = False, True

        if info.chart_type == 'line':
            layout = chart_styles(
                color_palette=single_color,
                title=info.title.upper(),
                **common_layout_args)

            traces = line_chart(
                df=info.data,
                line_smoothing=1,
                marker_size=10,
                mode='lines+markers'
            )

        else:
            layout = chart_styles(
                color_palette=multi_color,
                title=info.title.upper(),
                yaxis_showgrid=yaxis_grid,
                xaxis_showgrid=xaxis_grid,
                **common_layout_args
            )

            traces = bar_chart(
                df=info.data,
                orientation=info.orientation,
                marker_color=info.marker_colors
            )

        fig = display_chart(traces=traces, layout=layout)

        graph = dbc.Col([dcc.Graph(figure=fig)], width=info.width)
        charts.append(graph)
    return charts