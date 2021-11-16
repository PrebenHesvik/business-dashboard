from functools import partial
from plotly_chart_generator import chart_colors, display_chart

single_color = ["#5bb9ec"]
highlight_color = "#828438"
multi_color = chart_colors(
    palette_type="dark",
    color="#6bbaec",
    start_pos=3,
    step=2
)

common_layout_args = dict(
    bg_color="#2f323d",
    title_size=20,
    title_color="#BBBE64",
    showlegend=False,
)

display_chart = partial(display_chart, iplot=False)
