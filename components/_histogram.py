from dash import dcc, html
import plotly.graph_objects as go

from components.filtering import VARIABLE_LABELS, filter_sales


def build_histogram_figure(sales, borough, area_index, variable):
    """Show the selected variable for all sales matching the shared filters."""
    filtered = filter_sales(sales, borough, area_index)
    figure = go.Figure()
    if not filtered.empty:
        figure.add_trace(go.Histogram(
            x=filtered[variable].tolist(), nbinsx=50,
            marker={"color": "#42678c", "line": {"color": "#a0a9b3", "width": 0.5}},
            hovertemplate="%{x}<br>%{y} vendas<extra></extra>",
        ))
    else:
        figure.add_annotation(
            text="Nenhuma venda encontrada para os filtros selecionados.",
            x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False,
        )

    figure.update_layout(
        template="plotly_dark", paper_bgcolor="#151515", plot_bgcolor="#151515",
        font={"color": "#c7c7c7", "family": "Segoe UI, Arial, sans-serif", "size": 11},
        margin={"l": 52, "r": 12, "t": 12, "b": 44}, showlegend=False,
        bargap=0.05,
        xaxis={
            "title": VARIABLE_LABELS[variable], "gridcolor": "#262626",
            "tickprefix": "$" if variable == "SALE PRICE" else "",
        },
        yaxis={"title": "Vendas", "gridcolor": "#262626", "rangemode": "tozero"},
    )
    return figure

histogram = html.Section([
    html.Div([
        html.Div([
            html.H2("Sales distribution"),
            html.P("Compare the distribution of the selected variable"),
        ]),
        html.Span("02", className="chart-number"),
    ], className="section-heading"),
    dcc.Graph(
        id="histogram-graph", responsive=True,
        className="histogram-chart", config={"displayModeBar": False},
    ),
], className="panel chart-panel")
