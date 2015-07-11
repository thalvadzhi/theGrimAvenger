import unittest
import pygame
from pygame.math import Vector2 as Vector
from batarangs import Batarang
from environment import Block
from camera import Camera
pygame.init()
screen = pygame.display.set_mode((0, 0))


class BatarangTest(unittest.TestCase):
    def setUp(self):
        class World:
            def __init__(self, blocks=[], saws=[]):
                self.level_blocks = blocks
                self.level_saws = saws
        block = Block((0, 0, 0), 10, 10, 20, 10)
        world = World([block])
        self.camera = Camera(100, 100, 100, 100)
        self.batarang = Batarang(20, 10, world)

    def test_rotation(self):
        self.batarang.rotate(17)
        self.assertEqual(self.batarang.rotation, self.batarang.step)

    def test_movement(self):
        self.batarang.direction = Vector(0, 0)
        self.batarang.move(17)
        self.assertEqual(self.batarang.x, 20.0)
        self.assertEqual(self.batarang.y, 10.0)

        self.batarang.direction = Vector(1, 0)
        self.batarang.move(17)
        self.assertAlmostEqual(self.batarang.x, 28.50, 2)
        self.assertEqual(self.batarang.y, 10.0)

    def test_taking_action(self):
        self.batarang.take_action(self.camera)
        self.assertTrue(self.batarang.direction.x < 1)
        self.assertTrue(self.batarang.direction.y < 1)

    def test_update(self):
        self.batarang.should_fly = True
        self.batarang.update()
        self.assertEqual(self.batarang.rotation, self.batarang.step)
        self.assertEqual(self.batarang.x, 20.0)
        self.assertEqual(self.batarang.y, 10.0)
        self.batarang.direction = Vector(1, 0)
        self.batarang.move(17)
        self.assertAlmostEqual(self.batarang.x, 28.50, 2)
        self.assertEqual(self.batarang.y, 10.0)

    def test_repositioning(self):
        self.batarang.reposition((50, 50), Vector(1, 0))
        self.assertEqual(self.batarang.x, 50)
        self.assertEqual(self.batarang.y, 50)


if __name__ == '__main__':
    unittest.main()
