from dash import dcc, html

list_of_all_locations = {
    "All boroughs": 0, "Manhattan": 1, "Bronx": 2,
    "Brooklyn": 3, "Queens": 4, "Staten Island": 5,
}
slider_size = [100, 500, 1000, 10_000, 100_000, 1_000_000, 10_000_000]
area_labels = ["100", "500", "1 mil", "10 mil", "100 mil", "1 mi", "10 mi"]

borough_filter = html.Div([
    html.Label("Borough", htmlFor="borough-dropdown"),
    dcc.Dropdown(
        id="borough-dropdown",
        options=[{"label": name, "value": code} for name, code in list_of_all_locations.items()],
        value=0, clearable=False, className="dark-dropdown",
    ),
], className="filter-field")

area_filter = html.Div([
    html.Label("Maximum area (m²)", htmlFor="slider-square-size"),
    dcc.Slider(
        id="slider-square-size", min=0, max=len(slider_size) - 1,
        step=None, value=len(slider_size) - 1, allow_direct_input=False,
        className="area-slider",
        marks={
            index: {"label": label, "style": {"color": "#ffffff"}}
            for index, label in enumerate(area_labels)
        },
    ),
    html.P("Escala em m² · mil = 1.000 · mi = 1.000.000", className="filter-help"),
], className="filter-field filter-area")

variable_filter = html.Div([
    html.Label("Analysis variable", htmlFor="dropdown-color"),
    dcc.Dropdown(
        id="dropdown-color",
        options=[
            {"label": "Year built", "value": "YEAR BUILT"},
            {"label": "Total units", "value": "TOTAL UNITS"},
            {"label": "Sale price", "value": "SALE PRICE"},
        ],
        value="SALE PRICE", clearable=False, className="dark-dropdown",
    ),
], className="filter-field")

controllers = html.Section([
    html.Div(
        [html.H2("Filters"), html.P("Refine your market view")],
        className="section-heading",
    ),
    html.Div([borough_filter, area_filter, variable_filter], className="filters-grid"),
], className="panel filters-panel", **{"aria-label": "Market filters"})
