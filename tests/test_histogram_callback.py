import unittest

import pandas as pd

import index
from components import _histogram
from components.filtering import filter_sales


class DashboardCallbackTests(unittest.TestCase):
    def setUp(self):
        self.sales = pd.DataFrame({
            "BOROUGH": [1, 1, 2], "size_m2": [80, 600, 70],
            "SALE PRICE": [200_000, 900_000, 300_000],
            "YEAR BUILT": [1920, 1930, 1940], "TOTAL UNITS": [1, 2, 3],
        })

    def test_histogram_uses_shared_filtered_data(self):
        filtered = filter_sales(self.sales, 1, 0)
        figure = _histogram.build_histogram_figure(filtered, "YEAR BUILT")
        self.assertEqual(list(figure.data[0].x), [1920])

    def test_empty_histogram_has_a_message(self):
        figure = _histogram.build_histogram_figure(self.sales.iloc[:0], "SALE PRICE")
        self.assertEqual(len(figure.data), 0)
        self.assertTrue(figure.layout.annotations)

    def test_single_callback_updates_both_graphs_together(self):
        self.assertEqual(len(index.app.callback_map), 1)
        output = next(iter(index.app.callback_map))
        response = index.app.server.test_client().post("/_dash-update-component", json={
            "output": output,
            "outputs": [
                {"id": "histogram-graph", "property": "figure"},
                {"id": "map-graph", "property": "figure"},
            ],
            "inputs": [
                {"id": "borough-dropdown", "property": "value", "value": 3},
                {"id": "slider-square-size", "property": "value", "value": 1},
                {"id": "dropdown-color", "property": "value", "value": "TOTAL UNITS"},
            ],
            "state": [], "changedPropIds": ["borough-dropdown.value"],
        })
        self.assertEqual(response.status_code, 200)
        figures = response.get_json()["response"]
        histogram = figures["histogram-graph"]["figure"]
        map_figure = figures["map-graph"]["figure"]
        self.assertEqual(histogram["data"][0]["type"], "histogram")
        self.assertEqual(map_figure["data"][0]["type"], "scattermap")
        self.assertIsInstance(histogram["data"][0]["x"], list)
        self.assertIsInstance(map_figure["data"][0]["lat"], list)
        self.assertGreater(len(histogram["data"][0]["x"]), 0)
        self.assertNotIn("mapbox", map_figure["layout"])

    def test_original_values_remain_uncapped(self):
        self.assertGreater(index.df_data["SALE PRICE"].max(), 50_000_000)
        self.assertGreater(index.df_data["size_m2"].max(), 10_000)

    def test_missing_location_still_applies_area_filter(self):
        self.assertEqual(len(filter_sales(self.sales, None, 0)), 2)
