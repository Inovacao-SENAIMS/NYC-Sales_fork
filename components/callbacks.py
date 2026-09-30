from dash import Input, Output

from components._map import build_map_figure
from components._histogram import build_histogram_figure
from components.filtering import filter_sales


def register_dashboard_callback(app, df_data):
    """Filter once and return both figures in one response."""
    @app.callback(
        [Output("histogram-graph", "figure"), Output("map-graph", "figure")],
        [Input("borough-dropdown", "value"),
         Input("slider-square-size", "value"), Input("dropdown-color", "value")],
    )
    def update_hist(location, square_size, color_map):
        df_intermediate = filter_sales(df_data, location, square_size)
        color_map = color_map or "SALE PRICE"
        hist_fig = build_histogram_figure(df_intermediate, color_map)
        map_fig = build_map_figure(df_intermediate, color_map, df_data)
        return hist_fig, map_fig
