import dash
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.CYBORG], title="NYC | Real Estate Sales"
)
server = app.server
