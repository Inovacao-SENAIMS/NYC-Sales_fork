from dash import html

from app import app
from components._controllers import controllers
from components._histogram import histogram
from components._map import map
from components.callbacks import register_map_callback
from components.data_loader import load_sales_data

df_data = load_sales_data()

page_heading = html.Div([
    html.P("NEW YORK CITY · REAL ESTATE", className="eyebrow"),
    html.H1("Real Estate Sales Dashboard"),
    html.P(
        "Explore the NYC real estate market through interactive visualizations of sales data.",
        className="page-description",
    ),
])

page_header = html.Header([
    html.Div([
        html.Img(
            id="logo", src=app.get_asset_url("logo_dark.png"),
            alt="NYC Sales", className="brand-logo",
        ),
        page_heading,
    ], className="brand-heading"),
    html.Span("Market overview", className="header-tag"),
], className="page-header")

app.layout = html.Main([
    page_header,
    controllers,
    html.Div([map, histogram], className="charts-stack"),
    html.Footer(
        "NYC Real Estate Sales · Geographic overview & sales distribution",
        className="page-footer",
    ),
], className="dashboard-shell")

register_map_callback(app, df_data)

if __name__ == "__main__":
    app.run(debug=True, port=8050)
