import unittest
from Batarangs import Batarang
from pygame.math import Vector2 as Vector
import pygame
pygame.init()
screen = pygame.display.set_mode((0, 0))


class BatarangTest(unittest.TestCase):
    def setUp(self):
        self.batarang = Batarang(20, 10)

    def test_rotation(self):
        self.batarang.rotate(17)
        self.assertEqual(self.batarang.rotation, self.batarang.step)

    def test_movement(self):
        self.batarang.direction = Vector(0, 0)
        self.batarang.move(17)
        self.assertEqual(self.batarang.x, 8.0)
        self.assertEqual(self.batarang.y, 3.0)
        self.assertEqual(self.batarang.rect_center, (20.0, 10.0))

        self.batarang.direction = Vector(1, 0)
        self.batarang.move(17)
        self.assertAlmostEqual(self.batarang.x, 16.50, 2)
        self.assertEqual(self.batarang.y, 3.0)

        self.assertEqual(self.batarang.rect_center, (28.5, 10.0))

    def test_taking_action(self):
        self.batarang.take_action()
        self.assertTrue(self.batarang.direction.x < 1)
        self.assertTrue(self.batarang.direction.y < 1)

    def test_update(self):
        self.batarang.should_fly = True
        self.batarang.update(17)
        self.assertEqual(self.batarang.rotation, self.batarang.step)
        self.assertEqual(self.batarang.x, 8.0)
        self.assertEqual(self.batarang.y, 3.0)
        self.assertEqual(self.batarang.rect_center, (20.0, 10.0))
        self.batarang.direction = Vector(1, 0)
        self.batarang.move(17)
        self.assertAlmostEqual(self.batarang.x, 16.50, 2)
        self.assertEqual(self.batarang.y, 3.0)
        self.assertEqual(self.batarang.rect_center, (28.5, 10.0))

    def test_repositioning(self):
        self.batarang.reposition((50, 50), Vector(1, 0))
        self.assertEqual(self.batarang.rect.center, Vector(50, 50))
        self.assertEqual(self.batarang.x, 50)
        self.assertEqual(self.batarang.y, 50)


if __name__ == '__main__':
    unittest.main()