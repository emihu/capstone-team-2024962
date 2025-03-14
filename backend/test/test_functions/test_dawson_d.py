import unittest
import math

from src.utils.dawson_d import (
    distance_to_fov_path_1, distance_to_fov_path_2, puo, guo, check_within_fov,
    intersection_time, intersection_time_endpoint, start_end_intersection_time,
    d2, xacel, yacel, zacel, xaax, yaay, zaaz, d3
)

class TestMathFunctions(unittest.TestCase):

    def test_xacel(self):
        self.assertAlmostEqual(xacel(0, 0), 0.0)
        self.assertAlmostEqual(xacel(90, 0), -1.0)
        self.assertAlmostEqual(xacel(0, 90), 0.0)

    def test_yacel(self):
        self.assertAlmostEqual(yacel(0, 0), 0.0)
        self.assertAlmostEqual(yacel(90, 0), 0.0)
        self.assertAlmostEqual(yacel(0, 90), 0.0)

    def test_zacel(self):
        self.assertAlmostEqual(zacel(0), 1.0)
        self.assertAlmostEqual(zacel(90), 0.0)
        self.assertAlmostEqual(zacel(45), math.cos(math.pi / 4))

    def test_xaax(self):
        self.assertAlmostEqual(xaax(0, 0, 0), 0.0)
        self.assertAlmostEqual(xaax(90, 0, 0), -1.0)

    def test_yaay(self):
        self.assertAlmostEqual(yaay(0, 0, 0, 0), 0.0)

    def test_zaaz(self):
        self.assertAlmostEqual(zaaz(0, 0, 0, 0), 1.0)

    def test_distance_to_fov_path_1(self):
        self.assertGreaterEqual(distance_to_fov_path_1(math.radians(10), 0, 0, 0, 0, 1), 0.0)

    def test_distance_to_fov_path_2(self):
        self.assertGreaterEqual(distance_to_fov_path_2(math.radians(10), 0, 0, 0, 0, 1), 0.0)

    def test_puo(self):
        self.assertEqual(puo(0, 0, 0, 0, 0), 1)
        self.assertEqual(puo(0, 0, 0, 0, 90), 0)

    def test_guo(self):
        self.assertEqual(guo(0, 0, 0, 0, 0), 1)
        self.assertEqual(guo(0, 0, 0, 0, 90), 0)

    def test_check_within_fov(self):
        self.assertEqual(check_within_fov(math.radians(10), 0, 0, 0, 0), 1)
        self.assertEqual(check_within_fov(math.radians(10), 90, 90, 0, 0), 0)

    def test_intersection_time(self):
        self.assertEqual(intersection_time(0, 1), 1)
        self.assertEqual(intersection_time(2, 1), 0)

    def test_intersection_time_endpoint(self):
        self.assertEqual(intersection_time_endpoint(1, 1), 1)
        self.assertEqual(intersection_time_endpoint(1, 0), 0)

    def test_start_end_intersection_time(self):
        self.assertEqual(start_end_intersection_time(10, 1, 0, 0), 10)
        self.assertEqual(start_end_intersection_time(10, 0, 0, 0), 0)

    def test_d2(self):
        # Ensure function runs without error and returns no values
        self.assertIsNone(d2(10, 0, 0, 0, 0, 0))

    def test_d3(self):
        # Ensure function runs without error and returns no values
        self.assertIsNone(d3(0, 0, 0, 0))

if __name__ == '__main__':
    unittest.main()
