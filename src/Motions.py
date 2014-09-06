from pickle import dump, load
import os


class Motion:

    def __init__(self, item):
        self.__item = item
        self.frames = []

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
                motion.frames = load(motion_frames)

    def load_motion(self, path):
        with open(path, "rb") as motion_frames:
            self.frames = load(motion_frames)

    def save_motion(self, path):
        with open(path, 'wb') as motion_file:
            dump(self.frames, motion_file)

    def capture_frame(self):
        self.frames.append(self.item.capture_frame())

    def play_motion(self):
        self.frames[0] = self.item.capture_frame()
        for frame in range(len(self.frames) - 1):
            for _ in self.item.shift_to_next_frame(self.frames[frame],
                                                   self.frames[frame + 1]):
                yield frame
        # raise StopIteration

 #   def shift_to_next_frame(self, frames):
 #       for state in range(frames):
 #           yield
 #       self.current_frame += 1
