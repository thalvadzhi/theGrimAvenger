from pygame import *


class Camera:
    def __init__(self, width, height, window_width, window_height):
        self.state = Rect(0, 0, width, height)
        self.half_width = width // 2
        self.half_height = height // 2
        self.window_width = window_width
        self.window_height = window_height

    #this applies to sprites
    def apply(self, target):
        return target.rect.move(self.state.topleft)

    #this applies to rects
    def apply_to_rect(self, target):
        return target.move(self.state.topleft)

    #this updates sprites
    def update(self, target):
        self.state = self.functionality(target.rect)

    #this updates rects
    def update_rect(self, target):
        self.state = self.functionality(target)

    def functionality(self, target):
        left, top = target[0], target[1]
        left = self.half_width - left
        top = self.half_height - top
        #this is so as to not scroll the camera outside the borders of the level
        left = min(0, left)
        left = max((self.window_width - self.state.width), left)
        top = max((self.window_height - self.state.height), top)
        top = min(0, top)
        return Rect(left, top, self.state[2], self.state[3])
