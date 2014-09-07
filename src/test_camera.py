import unittest
from Camera import Camera
from pygame.math import Vector2 as Vector


class CameraTest(unittest.TestCase):
    def setUp(self):
        self.camera = Camera(800, 800, 10, 10)

    def test_apply(self):
        self.assertEqual(self.camera.apply((10, 10)), (10, 10))
        self.assertEqual(self.camera.apply(Vector((10, 10))), Vector(10, 10))
        self.assertEqual(self.camera.apply([Vector((10, 10)), Vector((5, 5))]),
                         [Vector((10, 10)), Vector((5, 5))])

    def test_update(self):
        self.camera.update((50, 50))
        self.assertEqual(self.camera.state.x, -45.0)
        self.camera.update(Vector((100, 100)))
        self.assertEqual(self.camera.state.x, -95.0)

    def test_reverse_apply(self):
        self.assertEqual(self.camera.reverse_apply((10, 10)), (10, 10))
        self.assertEqual(self.camera.reverse_apply(Vector((10, 10))),
                         Vector(10, 10))
        self.assertEqual(self.camera.reverse_apply([Vector((10, 10)),
                                                    Vector((5, 5))]),
                         [Vector((10, 10)), Vector((5, 5))])

    def test_functionality(self):
        self.assertEqual(self.camera.functionality((50, 50)).x, -45.0)
        self.assertEqual(self.camera.functionality((50, 50)).y, -45.0)

if __name__ == '__main__':
    unittest.main()
