import unittest
from pixelperfect import collide, get_hitmask
from basicshapes import Rectangle
import pygame
pygame.init()


class PixelPerfectTest(unittest.TestCase):
    def test_get_hitmask(self):
        rect = Rectangle(2, 2, (1, 1))
        image = pygame.Surface((2, 2))
        self.assertEqual(get_hitmask(rect, image, 0),
                         [[True, True], [True, True]])

    def test_collide(self):
        class Test:
            def __init__(self, rect, hitmask):
                self.rect = rect
                self.hitmask = hitmask

        rect2 = Rectangle(2, 2, (1, 2))
        rect1 = Rectangle(2, 2, (1, 1))
        sprite_a = Test(rect1, [[True, True], [True, True]])
        sprite_b = Test(rect2, [[True, True], [True, True]])
        rect2 = Rectangle(2, 2, (1, 15))
        self.assertEqual(collide(sprite_b, sprite_a), True)
        sprite_b = Test(rect2, [[True, True], [True, True]])
        self.assertEqual(collide(sprite_b, sprite_a), False)


if __name__ == '__main__':
    unittest.main()
