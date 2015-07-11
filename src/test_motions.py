import unittest

from ragdoll import HumanRagDoll
from motions import Motion


class MotionTests(unittest.TestCase):

    def setUp(self):
        self.item = HumanRagDoll()
        self.motion = Motion(self.item)

    # def test_capture_frame(self):
    #     body = RigitBody()
    #     apply_gravity(body, PHYSICS_SETTINGS["time_scale"])
    #     self.assertAlmostEqual(body.velocity.y, PHYSICS_SETTINGS["gravity"])

    # def test_apply_gravity_terminal_velocity(self):
    #     body = RigitBody()
    #     apply_gravity(body, PHYSICS_SETTINGS["time_scale"] * 1000000)
    #     self.assertAlmostEqual(
    #         body.velocity.y, PHYSICS_SETTINGS["terminal_velocity"])


if __name__ == "__main__":
    unittest.main()
