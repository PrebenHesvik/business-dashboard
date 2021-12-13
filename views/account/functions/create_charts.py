from dash import dcc
import dash_bootstrap_components as dbc

from plotly_chart_generator import (
    bar_chart,
    chart_styles,
)

from chart_configs import (
    single_color,
    multi_color,
    common_layout_args,
    display_chart
)


def create_charts(chart_data):
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
