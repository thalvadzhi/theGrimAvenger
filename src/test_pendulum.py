import unittest
from Pendulum import Pendulum

class PendulumTest(unittest.TestCase):
    def test_pendulum(self):
        bob = Pendulum(30, 30, (30, 30))
        bob.recompute_angle()
        self.assertAlmostEqual(bob.theta, 27.815, 3)
        self.assertAlmostEqual(bob.dtheta, -2.166, 3)

if __name__ == '__main__':
    unittest.main()

