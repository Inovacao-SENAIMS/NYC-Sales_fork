from dash import Input, Output

from components._map import build_map_figure
from components._histogram import build_histogram_figure


def register_map_callback(app, sales):
    """Connect the three existing filters to the map only."""
    @app.callback(
        Output("map-graph", "figure"),
        Input("borough-dropdown", "value"),
        Input("slider-square-size", "value"),
        Input("dropdown-color", "value"),
    )
    def update_map(borough, area_index, variable):
        return build_map_figure(sales, borough, area_index, variable)


def register_histogram_callback(app, sales):
    """Keep the histogram interactive through its own callback."""
    @app.callback(
        Output("histogram-graph", "figure"),
        Input("borough-dropdown", "value"),
        Input("slider-square-size", "value"),
        Input("dropdown-color", "value"),
    )
    def update_histogram(borough, area_index, variable):
        return build_histogram_figure(sales, borough, area_index, variable)
