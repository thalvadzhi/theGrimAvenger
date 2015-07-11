import unittest

from ragdoll import HumanRagdoll
from motions import Motion


class MotionTests(unittest.TestCase):

    pass
    # def setUp(self):
    #     self.item = HumanRagdoll()
    #     self.motion = Motion(self.item)

    # def test_capture_frame(self):
    #     self.item.set_slope(10)
    #     self.motion.capture_frame(3, 3)
    #     self.assertEqual(self.motion.duration, 3)
    #     self.assertNotEqual(len(self.motion.frames), 0)


if __name__ == "__main__":
    unittest.main()
