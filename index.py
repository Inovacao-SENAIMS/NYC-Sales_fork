# Import necessary libraries
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import app
import pandas as pd
from components._histogram import *
from components._map import *

# Data preprocessing
df_data = pd.read_csv('data\\cleaned_data.csv', index_col=0)
mean_lat = df_data['LATITUDE'].mean()
mean_lon = df_data['LONGITUDE'].mean()

df_data['size_m2']    = df_data["GROSS SQUARE FEET"] / 10.764
df_data               = df_data[df_data['YEAR BUILT'] > 0]
df_data['SALE DATE']  = pd.to_datetime(df_data['SALE DATE'], format='%Y-%m-%d')

df_data.loc[df_data["size_m2"] > 10000, "size_m2"] = 10000
df_data.loc[df_data["SALE PRICE"] > 50000000, "SALE PRICE"] = 50000000
df_data.loc[df_data["SALE PRICE"] > 10000, "SALE PRICE"] = 10000

# Layout of the app
app.layout = dbc.Container(
  children=[
    dbc.Row(
        children=[
            dbc.Col([], md=3),
            dbc.Col([map, histogram], md=9),
        ],
        )

  ], fluid=True, )

if __name__ == "__main__":
  app.run(debug=True, port=8050)