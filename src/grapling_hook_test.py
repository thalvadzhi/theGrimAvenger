import unittest
from graplinghook import GraplingHook
from environment import Block
from pygame.math import Vector2 as Vector
from pendulum import Pendulum
from camera import Camera
import pygame
pygame.init()
screen = pygame.display.set_mode((0, 0))


class GraplingHookTest(unittest.TestCase):
    def setUp(self):
        self.graple = GraplingHook(0, 0)

    def test_angle_calculation(self):
        self.graple.rope = Vector(0, -1)
        self.graple.calculate_angle()
        self.assertEqual(self.graple.angle, 90)
        self.graple.rope = Vector(0, 1)
        self.graple.calculate_angle()
        self.assertEqual(self.graple.angle, -90)
        self.graple.rope = Vector(1, 0)
        self.graple.calculate_angle()
        self.assertEqual(self.graple.angle, 0)

    def test_retraction(self):
        self.graple.distance = 200
        self.graple.rope = Vector(1, 0)
        self.graple.retract(17)
        self.assertEqual(self.graple.rect.center, Vector(11.9, 0.0))
        self.graple.distance = 200
        self.graple.rope = Vector(0, 1)
        self.graple.retract(17)
        self.assertEqual(self.graple.rect.center, Vector(11.9, 11.9))
        self.assertEqual(self.graple.x, -28.1)
        self.assertEqual(self.graple.y, -8.1)

    def test_rope_calculation(self):
        self.graple.rect.center = Vector(1, 0)
        self.graple.aim = Vector(0, 1)
        self.graple.calculate_rope()
        self.assertAlmostEqual(self.graple.distance, 1.41, 2)
        self.assertEqual(self.graple.rope,
                         Vector(-0.7071067811865475, 0.7071067811865475))

    def test_swinging(self):
        self.graple.bob = Pendulum(10, 1, (0, 0))
        self.graple.rope = Vector(1, 0)
        self.graple.swing()
        self.assertAlmostEqual(self.graple.step, -676.75, 2)
        self.assertEqual(self.graple.x, -40.0)
        self.assertEqual(self.graple.y, -20.0)
        self.assertEqual(self.graple.last_time, self.graple.current_time)

    def test_update(self):
        self.graple.shooter = True
        self.graple.should_retract = False
        self.graple.stop_rect = []
        self.graple.update(17, [], [])
        self.assertEqual(self.graple.x, self.graple.rect.x)
        self.assertEqual(self.graple.y, self.graple.rect.y)

    def test_functionality(self):
        class EVT:
            def __init__(self, event, key):
                self.type = event
                self.key = key
        events = [EVT(6, 1), EVT(4, 1), EVT(3, 306)]
        world = [Block((0, 0, 0), 500, 500, 0, 0)]
        self.graple.aim = (50, 50)
        self.graple.should_aim = True
        self.graple.functionality(events, world)
        self.assertEqual(self.graple.should_release, True)
        self.assertEqual(self.graple.should_retract, False)
        self.assertEqual(self.graple.shooter, True)

    def test_release(self):
        self.graple.bob = Pendulum(10, 1, (0, 0))
        self.graple.release(17)
        self.assertEqual(self.graple.rect.center, (0.0, 5.1000000000000005))

    def test_repositioning(self):
        self.graple.reposition((10, 10))
        self.assertEqual(self.graple.rect.center, Vector(10, 10))

    def test_drawing(self):
        self.graple.draw(screen, Camera(10, 10, 10, 10))

if __name__ == '__main__':
    unittest.main()
