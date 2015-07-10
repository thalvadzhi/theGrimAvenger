import os
from pickle import dump, load

import pygame

class Motion:

    LOADED = {}

    def __init__(self, item):
        self.__item = item
        self.frames = []
        self.is_repetitive = False
        self.name = ""
        self.current_motion = None
        self.paused = True
        self.action_frame = None
        self.on_action_frame = lambda : None
        self.speed_multiplier = 1

    @property
    def item(self):
        return self.__item

#    @classmethod
#    def load_motions(cls, folder):
#        motions = {}
#        for motion_file in os.listdir(folder):
#            motion = cls()
#            motions[motion_file[:len(motion_file) - 3]] = motion
#            with open(r"folder/{0}".format(motion_file),
#                      "rb") as motion_frames:
#                motion.frames = load(motion_frames)
    
    @classmethod
    def load(cls, path):
        motion_data = {}
        with open("../Files/Motions/{0}.motion".format(path), "rb") as motion:
            motion_data = load(motion)
        cls.LOADED[path] = motion_data

    def read_motion_data(self, data): 
        self.frames = data["frames"]
        self.is_repetitive = data["is_repetitive"]
        self.action_frame = data["action_frame"]

    def set_motion(self, name, speed_multiplier=1):
        self.name = name
        self.speed_multiplier = speed_multiplier
        if name not in Motion.LOADED:
            Motion.load(name)
        self.read_motion_data(Motion.LOADED[name])
        self.paused = False

    def save(self, path):
        motion_data = {
                "frames": self.frames,
                "is_repetitive": self.is_repetitive,
                "action_frame": self.action_frame
                }
        with open("../Files/Motions/{0}.motion".format(path), 'wb') as motion_file:
            dump(motion_data, motion_file)

    def capture_frame(self, order, duration=1):
        frame = self.item.capture_frame()
        frame["duration"] = duration
        if len(self.frames) <= order:
            self.frames.append(frame)
        else:
            self.frames[order] = frame

    def set_duration(self, frame, duration):
        self.frames[frame]["duration"] = duration

    def play_motion(self, start_time=0):
        yield
        if not start_time:
            start_time = pygame.time.get_ticks()
        for index, frame in enumerate(self.frames):
            if index == self.action_frame:
                self.on_action_frame()
            for _ in self.item.shift_to_frame(frame, start_time, self):
                start_time = _
                yield
            start_time += frame["duration"] // self.speed_multiplier
        return start_time

    def play(self):
        if self.current_motion is None:
            return
        try:
            next(self.current_motion)
        except StopIteration as finish_time:
            if self.is_repetitive:
                self.current_motion = self.play_motion(finish_time.value)
            else:
                self.current_motion = None
