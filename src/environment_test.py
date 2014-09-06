import unittest
import pygame
from Environment import Block, SawBlock, Shadow
from Vec2D import Vec2d as Vector
pygame.init()
screen = pygame.display.set_mode((0, 0))


class EnvironmentTest(unittest.TestCase):
    def test_block_setting_up(self):
        block = Block((0, 0, 0), 50, 50, 0, 0)
        block.load_texture()
        self.assertEqual(block.image.get_width(), block.width)
        block.load_texture("saw.png")
        self.assertEqual(block.image.get_width(), block.width)

    def test_saw_rotation(self):
        saw = SawBlock(50, 50, 150)
        saw.rotate_saw(17)
        self.assertEqual(saw.rotation, 5.1)
        saw.rotation = 500
        saw.rotate_saw(17)
        self.assertEqual(saw.rotation, saw.step)

    def test_swing_rope(self):
        saw = SawBlock(50, 50, 150)
        saw.swing_rope()
        self.assertEqual(saw.rect.center, (-55, 156))

    def test_deployment(self):
        saw = SawBlock(50, 50, 150)
        saw.bob.dtheta = 10
        saw.deploy()
        self.assertEqual(saw.is_severed, True)
        self.assertEqual(saw.direction, Vector(0.0, -1.0))

    def test_sign(self):
        saw = SawBlock(50, 50, 150)
        self.assertEqual(saw.sign(10), 1)
        self.assertEqual(saw.sign(-5), -1)

    def test_set_up(self):
        saw = SawBlock(50, 50, 150)
        saw.load_texture("saw.png")
        self.assertEqual(saw.image.get_width(), 50)

    def test_update(self):
        saw = SawBlock(50, 50, 150)
        saw.is_severed = True
        saw.velocity = Vector(1, 0)
        saw.update(17)
        self.assertEqual(saw.rect.center, (60.85090352453412, 215.5))
        saw.is_severed = False
        saw.update(17)
        self.assertEqual(saw.rect.center, (-55, 156))

    def test_collide_line(self):
        saw = SawBlock(10, 0, 5)
        saw.update(17)
        saw.update(17)

        self.assertEqual(saw.collide_line(2, 1), False)
        saw.x = 20
        self.assertEqual(saw.collide_line(2, 1), True)

    def test_collide(self):
        saw = SawBlock(10, 0, 5)

        class Bat:
            def __init__(self, x, y):
                self.x = x
                self.y = y
        saw.bob.dtheta = 20
        saw.collide(Bat(2, 1))

    def test_shadow(self):
        Shadow.load_texture(50, 50)
        shadow = Shadow((0, 0), (500, 0), (500, 500), (0, 500))
        self.assertEqual(shadow.collide([(50, 50)]), True)
        self.assertEqual(shadow.collide([(50, 50), (100, 100), (200, 200)]),
                         True)
        self.assertEqual(shadow.collide([(800, 50)]), False)

if __name__ == '__main__':
    unittest.main()
