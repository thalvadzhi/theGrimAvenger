import unittest
import pygame
from pygame.math import Vector2 as Vector
from environment import Block, SawBlock


pygame.init()
pygame.display.set_mode((1, 1))


class EnvironmentTest(unittest.TestCase):
    def setUp(self):
        self.saw = SawBlock(50, 50, 150)

    def test_saw_rotation(self):
        self.saw.rotate_saw(17)
        self.assertEqual(self.saw.rotation, 5.1)
        self.saw.rotation = 500
        self.saw.rotate_saw(17)
        self.assertEqual(self.saw.rotation, self.saw.step)

    def test_swing_rope(self):

        self.saw.swing_rope()
        self.assertEqual(self.saw.rect.center, (-55, 156))

    def test_deployment(self):
        self.saw.bob.d_theta = 10
        self.saw.deploy()
        self.assertEqual(self.saw.is_severed, True)
        self.assertEqual(self.saw.direction, Vector(0.0, -1.0))

    def test_sign(self):
        self.assertEqual(self.saw.sign(10), 1)
        self.assertEqual(self.saw.sign(-5), -1)

    def test_set_up(self):
        self.assertEqual(self.saw.image.get_width(), 50)

    def test_update(self):
        self.saw.is_severed = True
        self.saw.velocity = Vector(1, 0)
        self.saw.update(17)
        self.assertEqual(self.saw.rect.center, (60.85090352453412, 215.5))
        self.saw.is_severed = False
        self.saw.update(17)
        self.assertEqual(self.saw.rect.center, (-55, 156))

if __name__ == '__main__':
    unittest.main()
