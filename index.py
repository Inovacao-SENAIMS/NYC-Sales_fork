from dash import html

from app import app
from components._controllers import controllers
from components._histogram import histogram
from components._map import map
from components.callbacks import register_dashboard_callback
from components.data_loader import load_sales_data

df_data = load_sales_data()

sidebar = html.Aside([
    html.Header([
        html.Img(
            id="logo", src=app.get_asset_url("logo_dark.png"),
            alt="NYC Sales", className="brand-logo",
        ),
        html.P("NEW YORK CITY", className="eyebrow"),
        html.H1("Vendas de imóveis - NYC"),
        html.P(
            "Analise as vendas de imóveis em Nova Iorque "
            "entre setembro de 2016 e agosto de 2017.",
            className="page-description",
        ),
    ], className="sidebar-header"),
    controllers,
], className="dashboard-sidebar", **{"aria-label": "Identificação e filtros"})

app.layout = html.Main([
    sidebar,
    html.Div([map, histogram], className="charts-stack"),
], className="dashboard-shell")

register_dashboard_callback(app, df_data)

if __name__ == "__main__":
    app.run(debug=True, port=8050)
