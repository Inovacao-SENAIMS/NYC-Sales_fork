# Import necessary libraries
from dash import html
from app import app
import pandas as pd
from components._histogram import histogram
from components._map import map
from components._controllers import controllers

# Data preprocessing
df_data = pd.read_csv("data\\cleaned_data.csv", index_col=0)
mean_lat = df_data["LATITUDE"].mean()
mean_lon = df_data["LONGITUDE"].mean()

df_data["size_m2"] = df_data["GROSS SQUARE FEET"] / 10.764
df_data = df_data[df_data["YEAR BUILT"] > 0]
df_data["SALE DATE"] = pd.to_datetime(df_data["SALE DATE"], format="%Y-%m-%d")

df_data.loc[df_data["size_m2"] > 10000, "size_m2"] = 10000
df_data.loc[df_data["SALE PRICE"] > 50000000, "SALE PRICE"] = 50000000
df_data.loc[df_data["SALE PRICE"] > 10000, "SALE PRICE"] = 10000

# Layout of the app
app.layout = html.Main(
    [
        html.Header(
            [
                html.Div(
                    [
                        html.Img(
                            id="logo",
                            src=app.get_asset_url("logo_dark.png"),
                            alt="NYC Sales",
                            className="brand-logo",
                        ),
                        html.Div(
                            [
                                html.P(
                                    "NEW YORK CITY · REAL ESTATE", className="eyebrow"
                                ),
                                html.H1("Real Estate Sales Dashboard"),
                                html.P(
                                    "Explore the NYC real estate market through interactive visualizations of sales data.",
                                    className="page-description",
                                ),
                            ]
                        ),
                    ],
                    className="brand-heading",
                ),
                html.Span("Market overview", className="header-tag"),
            ],
            className="page-header",
        ),
        controllers,
        html.Div([map, histogram], className="charts-stack"),
        html.Footer(
            "NYC Real Estate Sales · Geographic overview & sales distribution",
            className="page-footer",
        ),
    ],
    className="dashboard-shell",
)

if __name__ == "__main__":
    app.run(debug=True, port=8050)
