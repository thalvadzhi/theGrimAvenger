import unittest

from basicshapes import RigitBody
from physics import *


class RigitBodyTest(unittest.TestCase):

    def test_apply_gravity(self):
        body = RigitBody()
        apply_gravity(body, PHYSICS_SETTINGS["time_scale"])
        self.assertAlmostEqual(body.velocity.y, PHYSICS_SETTINGS["gravity"])

    def test_apply_gravity_terminal_velocity(self):
        body = RigitBody()
        apply_gravity(body, PHYSICS_SETTINGS["time_scale"] * 1000000)
        self.assertAlmostEqual(
            body.velocity.y, PHYSICS_SETTINGS["terminal_velocity"])


if __name__ == "__main__":
    unittest.main()
