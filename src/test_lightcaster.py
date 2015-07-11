import unittest
from lightcaster import Line, Point, LightSource
from environment import Block


class LightcasterTest(unittest.TestCase):

    def test_line_intersection(self):
        left, right = Point(0, 0), Point(10, 0)
        top, bottom = Point(5, -5), Point(5, 5)
        top1, bottom1 = Point(6, -5), Point(6, 5)

        horizontal = Line(left, right)
        vertical = Line(top, bottom)
        parallel = Line(top1, bottom1)

        intersection = Line.get_intersection(horizontal, vertical)
        intersection1 = Line.get_intersection(vertical, parallel)
        self.assertIsNotNone(intersection)
        self.assertIsNone(intersection1)

    def test_light_cast(self):
        dimensions = [[Point(0, 0), Point(200, 0),
                       Point(200, 200), Point(0, 200)]]
        blocks = [[Point(10, 10), Point(20, 10),
                   Point(20, 20), Point(10, 20)]] + dimensions

        light = LightSource(10, 10, blocks)
        result = [(10.0, 10.0), (10.0, 10.0), (10.0, 10.0), (10.0, 10.0),
                  (10.0, 10.0), (10.0, 10.0), (10.0, 10.0), (10.0, 10.0),
                  (10.0, 10.0), (10.0, 10.0), (10.0, 10.0), (10.0, 10.0),
                  (10.0, 10.0), (10.0, 10.0), (10.0, 10.0), (10.0, 10.0),
                  (10.0, 10.0), (10.0, 10.0), (10.0, 10.0), (10.0, 10.0),
                  (10.0, 10.0), (10.0, 10.0), (10.0, 10.0)]
        visibility = light.cast()
        self.assertEqual(visibility, result)

if __name__ == '__main__':
    unittest.main()
