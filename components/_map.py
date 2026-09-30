from dash import html, dcc
import plotly.graph_objects as go

fig = go.Figure()
fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#151515",
    plot_bgcolor="#151515",
    font={"color": "#b5b5b5", "family": "Segoe UI, Arial, sans-serif"},
    margin={"l": 40, "r": 28, "t": 24, "b": 40},
    xaxis={"gridcolor": "#262626", "zerolinecolor": "#333333"},
    yaxis={"gridcolor": "#262626", "zerolinecolor": "#333333"},
)
map = html.Section(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.H2("Geographic overview"),
                        html.P("Property sales across the five boroughs"),
                    ]
                ),
                html.Span("01", className="chart-number"),
            ],
            className="section-heading",
        ),
        dcc.Graph(
            id="map-graph",
            figure=fig,
            responsive=True,
            className="map-chart",
            config={"displayModeBar": False, "scrollZoom": False},
        ),
    ],
    className="panel chart-panel",
)
