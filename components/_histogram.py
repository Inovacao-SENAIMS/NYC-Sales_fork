from dash import dcc, html
import plotly.graph_objects as go

fig = go.Figure()
fig.update_layout(
    template="plotly_dark", paper_bgcolor="#151515", plot_bgcolor="#151515",
    colorway=["#79b8aa", "#b3becb", "#d1b387"],
    font={"color": "#b5b5b5", "family": "Segoe UI, Arial, sans-serif"},
    margin={"l": 54, "r": 28, "t": 20, "b": 48},
    xaxis={"gridcolor": "#262626", "zerolinecolor": "#333333"},
    yaxis={"gridcolor": "#262626", "zerolinecolor": "#333333"},
)

histogram = html.Section([
    html.Div([
        html.Div([
            html.H2("Sales distribution"),
            html.P("Compare the distribution of the selected variable"),
        ]),
        html.Span("02", className="chart-number"),
    ], className="section-heading"),
    dcc.Graph(
        id="histogram-graph", figure=fig, responsive=True,
        className="histogram-chart", config={"displayModeBar": False},
    ),
], className="panel chart-panel")
