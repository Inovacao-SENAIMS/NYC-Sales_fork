import unittest

import pandas as pd

import index
from components import _histogram


class HistogramCallbackTests(unittest.TestCase):
    def setUp(self):
        self.sales = pd.DataFrame({
            "BOROUGH": [1, 1, 2], "size_m2": [80, 600, 70],
            "SALE PRICE": [200_000, 900_000, 300_000],
            "YEAR BUILT": [1920, 1930, 1940], "TOTAL UNITS": [1, 2, 3],
        })

    def test_histogram_uses_the_selected_variable_and_filters(self):
        self.assertTrue(hasattr(_histogram, "build_histogram_figure"))
        figure = _histogram.build_histogram_figure(self.sales, 1, 0, "YEAR BUILT")
        self.assertEqual(list(figure.data[0].x), [1920])

    def test_empty_histogram_has_a_message(self):
        self.assertTrue(hasattr(_histogram, "build_histogram_figure"))
        figure = _histogram.build_histogram_figure(self.sales, 5, 0, "SALE PRICE")
        self.assertEqual(len(figure.data), 0)
        self.assertTrue(figure.layout.annotations)

    def test_histogram_callback_returns_data(self):
        self.assertIn("histogram-graph.figure", index.app.callback_map)
        response = index.app.server.test_client().post("/_dash-update-component", json={
            "output": "histogram-graph.figure",
            "outputs": {"id": "histogram-graph", "property": "figure"},
            "inputs": [
                {"id": "borough-dropdown", "property": "value", "value": 3},
                {"id": "slider-square-size", "property": "value", "value": 1},
                {"id": "dropdown-color", "property": "value", "value": "TOTAL UNITS"},
            ],
            "state": [], "changedPropIds": ["borough-dropdown.value"],
        })
        self.assertEqual(response.status_code, 200)
        figure = response.get_json()["response"]["histogram-graph"]["figure"]
        self.assertEqual(figure["data"][0]["type"], "histogram")
        self.assertGreater(len(figure["data"][0]["x"]), 0)
