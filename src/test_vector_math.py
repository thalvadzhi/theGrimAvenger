import unittest

from pygame.math import Vector2 as Vector

from vectormath import *


def round_vector(vector, decimal=0):
    return Vector(round(vector.x, decimal), round(vector.y, decimal))


class FunctionsTest(unittest.TestCase):

    def test_check_if_parallel(self):
        self.assertTrue(check_if_parallel(Vector(1, 0), Vector(2, 0)))
        self.assertFalse(check_if_parallel(Vector(1, 0), Vector(2, 1)))

    def test_point_in_same_direction(self):
        self.assertTrue(point_in_same_direction(Vector(1, 0), Vector(2, 0)))
        self.assertFalse(point_in_same_direction(Vector(-1, 0), Vector(2, 0)))

    def test_calculate_centroid(self):
        self.assertEqual(Vector(1, 0), round_vector(calculate_centroid([
            Vector(1, 1), Vector(1, -1)])))


class LineTest(unittest.TestCase):

    def setUp(self):
        self.line = Line(Vector(0, 0), Vector(1, 0))
        self.segment = Line(Vector(0, 0), Vector(1, 0), True)

    def test_calulate_line_equation(self):
        line_equation = self.line.calculate_line_equation()
        self.assertEqual(round_vector(Vector(line_equation)), Vector(0, 0))

    def test_check_if_parallel(self):
        self.assertTrue(self.line.check_if_parallel(self.segment))
        self.assertFalse(self.line.check_if_parallel(
            Line(Vector(1, 1), Vector(0, 0))))

    def test_get_normal(self):
        self.assertEqual(round(self.line.get_normal().length()), 1)
        self.assertTrue(
            check_if_parallel(self.line.get_normal(), Vector(0, 1)))

    def test_reflect_point(self):
        self.assertEqual(
            round_vector(self.line.reflect_point(Vector(1, -1))), Vector(1, 1))

    def test_check_if_point_belongs(self):
        self.assertFalse(self.segment.check_if_point_belongs(Vector(1000, 0)))
        self.assertTrue(self.segment.check_if_point_belongs(Vector(0.5, 0)))

    def test_calculate_altitude_foot(self):
        self.assertEqual(round_vector(Line(
            Vector(3, 3), Vector(3, 8)).calculate_altitude_foot(Vector(2, 2))),
            Vector(3, 2))
        self.assertEqual(
            round_vector(self.line.calculate_altitude_foot(Vector(2, 2))),
            Vector(2, 0))
        self.assertEqual(round_vector(Line(
            Vector(0, 0), Vector(1, 1)).calculate_altitude_foot(Vector(2, 2))),
            Vector(2, 2))

    def test_check_if_intersects_line(self):
        self.assertTrue(self.line.check_if_intersects_line(Line(
            Vector(3, 3), Vector(3, 8))))

    def test_get_closest_point(self):
        closest = round_vector(self.line.get_closest_point(Vector(1, 1)))
        self.assertEqual(closest, Vector(1, 0))
        closest = round_vector(self.segment.get_closest_point(Vector(2, 2)))
        self.assertEqual(closest, Vector(1, 0))
        closest = round_vector(self.segment.get_closest_point(Vector(-2, -2)))
        self.assertEqual(closest, Vector(0, 0))

    def test_calculate_point_of_intersection(self):
        self.assertEqual(
            self.line.calculate_point_of_intersection(self.segment), None)
        self.assertEqual(round_vector(
            self.segment.calculate_point_of_intersection(Line(
                Vector(0.01, 0), Vector(1, 1)))), Vector(0, 0))
        self.assertEqual(
            self.segment.calculate_point_of_intersection(Line(
                Vector(-0.1, 0), Vector(1, 1))), None)

if __name__ == "__main__":
    unittest.main()
