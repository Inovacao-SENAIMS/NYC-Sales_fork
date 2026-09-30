from dash import dcc, html
from math import asinh, degrees, log2, pi, radians, sinh, atan, tan

import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import get_colorscale

from components.filtering import VARIABLE_LABELS, filter_sales


def map_view(located):
    """Fit the extent using Web Mercator, including narrow/mobile map widths."""
    if located.empty:
        return {"lat": 40.70, "lon": -73.94}, 9

    west, east = located["LONGITUDE"].min(), located["LONGITUDE"].max()
    south, north = located["LATITUDE"].min(), located["LATITUDE"].max()
    mercator_south = asinh(tan(radians(south)))
    mercator_north = asinh(tan(radians(north)))
    center = {
        "lat": degrees(atan(sinh((mercator_south + mercator_north) / 2))),
        "lon": (west + east) / 2,
    }
    longitude_span = max((east - west) / 360, 0.00001)
    latitude_span = max((mercator_north - mercator_south) / (2 * pi), 0.00001)
    zoom = min(log2(280 / (512 * longitude_span)), log2(320 / (512 * latitude_span)))
    return center, min(14, max(0, zoom - 0.3))


def build_map_figure(sales, borough, area_index, variable):
    """Filter sales and plot usable coordinates within the NYC bounding box."""
    filtered = filter_sales(sales, borough, area_index)

    located = filtered.loc[
        filtered["LATITUDE"].between(40.49, 40.93)
        & filtered["LONGITUDE"].between(-74.26, -73.68)
    ]
    figure = go.Figure()
    if not located.empty:
        price_format = "$,.0f" if variable == "SALE PRICE" else ",.0f"
        figure = px.scatter_map(
            located, lat="LATITUDE", lon="LONGITUDE", color=variable,
            map_style="carto-darkmatter",
            hover_name="ADDRESS",
            custom_data=["SALE PRICE", "size_m2", "YEAR BUILT", "TOTAL UNITS"],
        )
        # Plotly 6 may include a legacy mapbox layout; keep only the MapLibre map.
        figure.layout.mapbox = None
        # Use explicit lists for predictable Dash payloads and one shared color legend.
        figure.update_traces(
            lat=located["LATITUDE"].tolist(),
            lon=located["LONGITUDE"].tolist(),
            text=located["ADDRESS"].tolist(),
            customdata=located[["SALE PRICE", "size_m2", "YEAR BUILT", "TOTAL UNITS"]].values.tolist(),
            mode="markers",
            marker={
                "size": 9, "opacity": 0.8, "color": located[variable].tolist(),
                "coloraxis": None,
                "colorscale": get_colorscale("Rainbow"),
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
        )
        figure.update_layout(coloraxis_showscale=False)

    center, zoom = map_view(located)

    figure.update_layout(
        template="plotly_dark", paper_bgcolor="#151515", plot_bgcolor="#151515",
        font={"color": "#d5d5d5", "family": "Segoe UI, Arial, sans-serif"},
        margin={"l": 0, "r": 0, "t": 34, "b": 0},
        map={"style": "carto-darkmatter", "center": center, "zoom": zoom},
        uirevision=f"filters-{borough}-{area_index}", showlegend=False,
        dragmode="pan",
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
        config={"displayModeBar": False, "scrollZoom": True},
    ),
], className="panel chart-panel")
