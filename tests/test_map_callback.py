import unittest

import pandas as pd

from components import _map
from components.filtering import filter_sales


class MapCallbackTests(unittest.TestCase):
    def setUp(self):
        self.sales = pd.DataFrame({
            "BOROUGH": [1, 1, 2, 1, 1], "size_m2": [80, 600, 70, 50, 60],
            "LATITUDE": [40.75, 40.76, 40.85, None, 51.63],
            "LONGITUDE": [-73.98, -73.97, -73.90, None, 151.35],
            "SALE PRICE": [200_000, 900_000, 300_000, 400_000, 500_000],
            "YEAR BUILT": [1920, 1930, 1940, 1950, 1960],
            "TOTAL UNITS": [1, 2, 3, 4, 5], "ADDRESS": ["A", "B", "C", "D", "E"],
        })

    def test_borough_and_square_meter_filters(self):
        original = self.sales.copy(deep=True)
        filtered = filter_sales(self.sales, 1, 0)
        figure = _map.build_map_figure(filtered, "SALE PRICE", self.sales)
        self.assertEqual(list(figure.data[0].lat), [40.75])
        self.assertEqual(list(figure.data[0].marker.color), [200_000])
        pd.testing.assert_frame_equal(self.sales, original)

    def test_marker_sizes_follow_area_instead_of_price(self):
        figure = _map.build_map_figure(self.sales, "SALE PRICE", self.sales)
        sizes = list(figure.data[0].marker.size)
        self.assertLess(sizes[2], sizes[0])
        self.assertLess(sizes[0], sizes[1])
        self.assertAlmostEqual(min(sizes), 8)
        self.assertAlmostEqual(max(sizes), 24)

    def test_quantile_color_scale_is_stable_across_filters(self):
        wide = _map.build_map_figure(self.sales, "SALE PRICE", self.sales)
        narrow = _map.build_map_figure(self.sales.iloc[:1], "SALE PRICE", self.sales)
        self.assertEqual(wide.layout.coloraxis.colorscale, narrow.layout.coloraxis.colorscale)
        self.assertEqual(wide.layout.coloraxis.cmin, 200_000)
        self.assertEqual(wide.layout.coloraxis.cmax, 900_000)

    def test_constant_variable_has_a_valid_scale(self):
        sales = self.sales.copy()
        sales["TOTAL UNITS"] = 1
        figure = _map.build_map_figure(sales, "TOTAL UNITS", sales)
        self.assertTrue(figure.to_json())
        self.assertGreater(figure.layout.coloraxis.cmax, figure.layout.coloraxis.cmin)

    def test_empty_map_has_a_message(self):
        figure = _map.build_map_figure(self.sales.iloc[:0], "SALE PRICE", self.sales)
        self.assertEqual(len(figure.data), 0)
        self.assertIn("No sales", figure.layout.annotations[0].text)

    def test_zoom_adapts_to_extent(self):
        wide = _map.build_map_figure(self.sales, "SALE PRICE", self.sales)
        narrow = _map.build_map_figure(self.sales.iloc[:1], "SALE PRICE", self.sales)
        self.assertGreater(narrow.layout.map.zoom, wide.layout.map.zoom)
