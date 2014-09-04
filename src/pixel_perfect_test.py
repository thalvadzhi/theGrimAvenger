import unittest
from pixelperfect import collide, get_hitmask
from BasicShapes import Rectangle
import pygame
pygame.init()


class PendulumTest(unittest.TestCase):
    def test_get_hitmask(self):
        rect = Rectangle(2, 2, (1, 1))
        image = pygame.Surface((2, 2))
        self.assertEqual(get_hitmask(rect, image,0), [[True, True], [True, True]])

    def test_collide(self):
        rect1 = Rectangle(2, 2, (1, 1))
        rect2 = Rectangle(2, 2, (1, 2))
        image = pygame.Surface((2, 2))
        self.assertEqual(collide(rect1, [[True, True], [True, True]], rect2, [[True, True], [True, True]]), True)
        rect2 = Rectangle(2, 2, (1, 15))
        self.assertEqual(collide(rect1, [[True, True], [True, True]], rect2, [[True, True], [True, True]]), False)
        rect2 = Rectangle(0, 0, (0, 0))


if __name__ == '__main__':
    unittest.main()

