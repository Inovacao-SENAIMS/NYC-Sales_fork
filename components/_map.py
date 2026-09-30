from dash import dcc, html
import plotly.graph_objects as go

from components._controllers import slider_size

VARIABLE_LABELS = {
    "SALE PRICE": "Sale price (USD)",
    "YEAR BUILT": "Year built",
    "TOTAL UNITS": "Total units",
}


def build_map_figure(sales, borough, area_index, variable):
    """Filter sales and plot usable coordinates within the NYC bounding box."""
    area_limit = slider_size[area_index if area_index is not None else -1]
    filtered = sales.loc[sales["size_m2"] <= area_limit]
    if borough:
        filtered = filtered.loc[filtered["BOROUGH"] == borough]

    located = filtered.loc[
        filtered["LATITUDE"].between(40.49, 40.93)
        & filtered["LONGITUDE"].between(-74.26, -73.68)
    ]
    figure = go.Figure()
    if not located.empty:
        price_format = "$,.0f" if variable == "SALE PRICE" else ",.0f"
        figure.add_trace(go.Scattermap(
            lat=located["LATITUDE"].tolist(),
            lon=located["LONGITUDE"].tolist(),
            text=located["ADDRESS"].tolist(),
            customdata=located[["SALE PRICE", "size_m2", "YEAR BUILT", "TOTAL UNITS"]].values.tolist(),
            mode="markers",
            marker={
                "size": 7, "opacity": 0.8, "color": located[variable].tolist(),
                "colorscale": [[0, "#707070"], [0.5, "#b5b5b5"], [1, "#ffffff"]],
                "showscale": True,
                "colorbar": {
                    "title": VARIABLE_LABELS[variable], "tickformat": price_format,
                    "thickness": 12, "len": 0.8,
                },
            },
            hovertemplate=(
                "<b>%{text}</b><br>Sale price: $%{customdata[0]:,.0f}"
                "<br>Area: %{customdata[1]:,.1f} m²"
                "<br>Year built: %{customdata[2]:.0f}"
                "<br>Total units: %{customdata[3]:.0f}<extra></extra>"
            ),
        ))

    center = {"lat": 40.70, "lon": -73.94}
    if not located.empty:
        center = {"lat": located["LATITUDE"].median(), "lon": located["LONGITUDE"].median()}

    figure.update_layout(
        template="plotly_dark", paper_bgcolor="#151515", plot_bgcolor="#151515",
        font={"color": "#d5d5d5", "family": "Segoe UI, Arial, sans-serif"},
        margin={"l": 0, "r": 0, "t": 34, "b": 0},
        map={"style": "carto-darkmatter", "center": center, "zoom": 10 if borough else 9},
        uirevision=f"borough-{borough}", showlegend=False,
    )
    if located.empty:
        message = "No sales with usable NYC coordinates match these filters."
    else:
        missing = len(filtered) - len(located)
        message = f"{len(located):,} sales on the map · {missing:,} without usable NYC coordinates"
    figure.add_annotation(
        text=message, x=0, y=1.04, xref="paper", yref="paper",
        xanchor="left", showarrow=False, font={"size": 12, "color": "#c7c7c7"},
    )
    return figure


map = html.Section([
    html.Div([
        html.Div([
            html.H2("Geographic overview"),
            html.P("Property sales across the five boroughs"),
        ]),
        html.Span("01", className="chart-number"),
    ], className="section-heading"),
    dcc.Graph(
        id="map-graph", responsive=True, className="map-chart",
        config={"displayModeBar": False, "scrollZoom": False},
    ),
], className="panel chart-panel")
