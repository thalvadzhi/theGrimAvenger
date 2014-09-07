import unittest

from pygame.math import Vector2 as Vector

from VectorMath import *


def round_vector(vector, decimal=0):
    return Vector(round(vector.x, decimal), round(vector.y, decimal))


class FunctionsTest(unittest.TestCase):

    def test_check_if_parallel(self):
        self.assertTrue(check_if_parallel(Vector(1, 0), Vector(2, 0)))
        self.assertFalse(check_if_parallel(Vector(1, 0), Vector(2, 1)))

    def test_point_in_same_direction(self):
        self.assertTrue(check_if_parallel(Vector(1, 0), Vector(2, 0)))
        self.assertFalse(check_if_parallel(Vector(-1, 0), Vector(2, 0)))

    def test_calculate_centroid(self):
        self.assertEqual(Vector(1, 0), round_vector(calculate_centroid([
            Vector(1, 1), Vector(1, -1)])))

class LineTest(unittest.TestCase):

    def setUp(self):
        self.line = Line(Vector(0, 0), Vector(1, 0))
        self.segment = Line(Vector(0, 0), Vector(1, 0), True)

    def test_calulate_line_equation(self):
        line_equation = self.line.calculate_line_equation()
