from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import app
import pandas as pd

df_data = pd.read_csv('data/cleaned_data.csv', index_col=0)
mean_lat = df_data['LATITUDE'].mean()
mean_lon = df_data['LONGITUDE'].mean()

df_data['size_m2'] = df_data["GROSS SQUARE FEET"] / 10.764
df_data = df_data[df_data['YEAR BUILT'] > 0]
df_data['SALE DATE'] = pd.to_datetime(df_data['SALE DATE'], format='%m/%d/%Y')


app.layout = dbc.Container(
  children=[
    
  ], fluid=True, )

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)