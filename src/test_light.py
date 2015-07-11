import unittest
import pygame
from environment import Block
from light import Light

pygame.init()
pygame.display.set_mode((1, 1))

class LightTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Light.set_up_surfaces(32, 32)
        cls.result = [(10.0, 10.0), (10.0, 10.0), (10.0, 10.0), (10.0, 10.0),
                      (10.0, 10.0), (10.0, 10.0), (10.0, 10.0), (10.0, 10.0),
                      (10.0, 10.0), (10.0, 10.0), (10.0, 10.0), (10.0, 10.0),
                      (10.0, 10.0), (10.0, 10.0), (10.0, 10.0), (10.0, 10.0),
                      (10.0, 10.0), (10.0, 10.0), (10.0, 10.0), (10.0, 10.0),
                      (10.0, 10.0), (10.0, 10.0), (10.0, 10.0)]

    def test_casting(self):
        light = Light(10, 10, 50)
        light.update()
        visibitlity = light.visibility
        result = [(0.0, 0.00019999800003844825), (0.0, 0.0),
                  (0.00019999800003844825, 0.0), (31.99941601284763, 0.0),
                  (32.0, 7.105427357601002e-15), (32.0, 0.0002654533388604108),
                  (32.0, 31.999560004399918), (32.0, 32.0),
                  (31.999560004399914, 32.0),
                  (0.00026545333886218714, 31.999999999999996),
                  (7.105427357601002e-15, 32.0), (0.0, 31.999416012847632)]
        self.assertEqual(result, visibitlity)

    def test_casting_with_obstacles(self):
        block = Block((0, 0, 0), 10, 10, 10, 10)
        light = Light(10, 10, 50, [block])
        light.update()
        visibitlity = light.visibility

        self.assertEqual(visibitlity, self.result)

    def test_update_obstacles(self):
        block = Block((0, 0, 0), 10, 10, 10, 10)
        light = Light(10, 10, 50)
        light.update_obstacles([block])
        visibility = light.visibility
        self.assertEqual(visibility, self.result)

    def test_update_light_position(self):
        block = Block((0, 0, 0), 10, 10, 10, 10)
        light = Light(5, 5, 50, [block])
        light.update_light_position(10, 10)
        visibility = light.visibility
        self.assertEqual(visibility, self.result)

    def test_collide(self):
        light = Light(10, 10, 50)
        self.assertTrue(light.collide((10, 10)))
        self.assertFalse(light.collide((60, 60)))

    def test_is_illuminated(self):
        block = Block((0, 0, 0), 10, 10, 10, 10)
        light = Light(5, 5, 50, [block])
        light.update()
        self.assertTrue(light.is_illuminated([(6, 6)]))


if __name__ == '__main__':
    unittest.main()
