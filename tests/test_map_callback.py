import unittest

import pandas as pd

import index
from components import _map


class MapCallbackTests(unittest.TestCase):
    def setUp(self):
        self.sales = pd.DataFrame({
            "BOROUGH": [1, 1, 2, 1, 1],
            "size_m2": [80, 600, 70, 50, 60],
            "LATITUDE": [40.75, 40.76, 40.85, None, 51.63],
            "LONGITUDE": [-73.98, -73.97, -73.90, None, 151.35],
            "SALE PRICE": [200_000, 900_000, 300_000, 400_000, 500_000],
            "YEAR BUILT": [1920, 1930, 1940, 1950, 1960],
            "TOTAL UNITS": [1, 2, 3, 4, 5],
            "ADDRESS": ["A", "B", "C", "D", "E"],
        })

    def test_map_combines_borough_and_area_filters(self):
        self.assertTrue(hasattr(_map, "build_map_figure"), "Map builder is missing")
        original = self.sales.copy(deep=True)
        figure = _map.build_map_figure(self.sales, 1, 0, "SALE PRICE")
        self.assertEqual(list(figure.data[0].lat), [40.75])
        self.assertEqual(list(figure.data[0].marker.color), [200_000])
        pd.testing.assert_frame_equal(self.sales, original)

    def test_variable_changes_marker_colors(self):
        self.assertTrue(hasattr(_map, "build_map_figure"), "Map builder is missing")
        figure = _map.build_map_figure(self.sales, 0, 6, "TOTAL UNITS")
        self.assertEqual(list(figure.data[0].marker.color), [1, 2, 3])
        self.assertEqual(figure.data[0].marker.colorbar.title.text, "Total units")

    def test_larger_values_produce_larger_markers(self):
        figure = _map.build_map_figure(self.sales, 0, 6, "SALE PRICE")
        sizes = list(figure.data[0].marker.size)
        self.assertLess(sizes[0], sizes[2])
        self.assertLess(sizes[2], sizes[1])
        self.assertAlmostEqual(min(sizes), 8)
        self.assertAlmostEqual(max(sizes), 24)

    def test_equal_values_produce_finite_equal_marker_sizes(self):
        sales = self.sales.copy()
        sales["TOTAL UNITS"] = 1
        figure = _map.build_map_figure(sales, 0, 6, "TOTAL UNITS")
        sizes = list(figure.data[0].marker.size)
        self.assertEqual(sizes, [8, 8, 8])

    def test_empty_results_have_an_explanation(self):
        self.assertTrue(hasattr(_map, "build_map_figure"), "Map builder is missing")
        figure = _map.build_map_figure(self.sales, 5, 0, "SALE PRICE")
        self.assertEqual(len(figure.data), 0)
        self.assertIn("No sales", figure.layout.annotations[0].text)

    def test_real_prices_and_areas_are_not_capped(self):
        self.assertGreater(index.df_data["SALE PRICE"].max(), 50_000_000)
        self.assertGreater(index.df_data["size_m2"].max(), 10_000)

    def test_dash_serves_the_map_callback(self):
        self.assertIn("map-graph.figure", index.app.callback_map)
        response = index.app.server.test_client().post("/_dash-update-component", json={
            "output": "map-graph.figure",
            "outputs": {"id": "map-graph", "property": "figure"},
            "inputs": [
                {"id": "borough-dropdown", "property": "value", "value": 1},
                {"id": "slider-square-size", "property": "value", "value": 0},
                {"id": "dropdown-color", "property": "value", "value": "YEAR BUILT"},
            ],
            "state": [],
            "changedPropIds": ["borough-dropdown.value"],
        })
        self.assertEqual(response.status_code, 200)
        figure = response.get_json()["response"]["map-graph"]["figure"]
        self.assertEqual(figure["data"][0]["type"], "scattermap")
        self.assertEqual(figure["layout"]["map"]["style"], "carto-darkmatter")
        self.assertNotIn("mapbox", figure["layout"])

    def test_zoom_adapts_to_geographic_extent(self):
        wide = _map.build_map_figure(self.sales, 0, 6, "SALE PRICE")
        narrow = _map.build_map_figure(self.sales, 1, 0, "SALE PRICE")
        self.assertGreater(narrow.layout.map.zoom, wide.layout.map.zoom)


if __name__ == "__main__":
    unittest.main()
