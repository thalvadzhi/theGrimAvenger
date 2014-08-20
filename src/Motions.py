import pickle
import os

from pygame.math import Vector2 as Vector


class Motion:

    def __init__(self, item):
        self.__item = item
        self.current_frame = 0
        self.frames = {}

    @property
    def item(self):
        return self.__item

    @classmethod
    def load_motions(cls, folder):
        motions = {}
        for motion_file in os.listdir(folder):
            motion = cls()
            motions[motion_file[:len(motion_file) - 3]] = motion
            with open(r"folder/{0}".format(motion_file),
                      "rb") as motion_frames:
                motion.frames = pickle.load(motion_frames)

    def save_motion(self, path):
        with open(path, 'wb') as motion_file:
            pickle.dump(self.frames, motion_file)

    def capture_frame(self):
        self.frames[len(
            self.frames.keys()) + 1] = self.item.convert_to_local_coordinates()

    def play_motion(self, fps):
        for frame in self.frames.keys():
            self.

    def shift_to_next_frame(self, frames):
        for state in range(frames):
            yield
        self.current_frame += 1
