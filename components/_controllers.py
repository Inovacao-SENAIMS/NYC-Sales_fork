from dash import html, dcc

list_of_all_locations = {
    "All boroughs": 0,
    "Manhattan": 1,
    "Bronx": 2,
    "Brooklyn": 3,
    "Queens": 4,
    "Staten Island": 5,
}
slider_size = [100, 500, 1000, 10_000, 100_000, 1_000_000, 10_000_000]

controllers = html.Section(
    [
        html.Div(
            [html.H2("Filters"), html.P("Refine your market view")],
            className="section-heading",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Borough", htmlFor="borough-dropdown"),
                        dcc.Dropdown(
                            id="borough-dropdown",
                            options=[
                                {"label": k, "value": v}
                                for k, v in list_of_all_locations.items()
                            ],
                            value=0,
                            clearable=False,
                            className="dark-dropdown",
                        ),
                    ],
                    className="filter-field",
                ),
                html.Div(
                    [
                        html.Label("Maximum area (m²)", htmlFor="slider-square-size"),
                        dcc.Slider(
                            id="slider-square-size",
                            min=0,
                            max=len(slider_size) - 1,
                            step=None,
                            value=len(slider_size) - 1,
                            allow_direct_input=False,
                            className="area-slider",
                            marks={
                                index: {
                                    "label": label,
                                    "style": {"color": "#ffffff"},
                                }
                                for index, label in enumerate(
                                    [
                                        "100",
                                        "500",
                                        "1 mil",
                                        "10 mil",
                                        "100 mil",
                                        "1 mi",
                                        "10 mi",
                                    ]
                                )
                            },
                        ),
                        html.P(
                            "Escala em m² · mil = 1.000 · mi = 1.000.000",
                            className="filter-help",
                        ),
                    ],
                    className="filter-field filter-area",
                ),
                html.Div(
                    [
                        html.Label("Analysis variable", htmlFor="dropdown-color"),
                        dcc.Dropdown(
                            id="dropdown-color",
                            options=[
                                {"label": label, "value": value}
                                for label, value in [
                                    ("Year built", "YEAR BUILT"),
                                    ("Total units", "TOTAL UNITS"),
                                    ("Sale price", "SALE PRICE"),
                                ]
                            ],
                            value="SALE PRICE",
                            clearable=False,
                            className="dark-dropdown",
                        ),
                    ],
                    className="filter-field",
                ),
            ],
            className="filters-grid",
        ),
    ],
    className="panel filters-panel",
    **{"aria-label": "Market filters"},
)
