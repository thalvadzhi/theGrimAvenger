from pygame import *
from pygame.math import Vector2 as Vector

class Camera:
    def __init__(self, width, height, window_width, window_height):
        self.state = Rect(0, 0, width, height)
        self.half_width = window_width // 2
        self.half_height = window_height // 2
        self.window_width = window_width
        self.window_height = window_height

    #this applies to sprites
    def apply(self, target):
        return target.rect.move(self.state.topleft)

    #this applies to rects
    def apply_to_rect(self, target):
        return target.move(self.state.topleft)

    def apply_to_tuple(self, target):
        result_x = target[0] + self.state.x
        result_y = target[1] + self.state.y
        return result_x, result_y

    def reverse_apply(self, target):
        result_x = target[0] - self.state.x
        result_y = target[1] - self.state.y
        return result_x, result_y

    def apply_to_vertices(self, vertices):
        for vertex in vertices:
            vertex.x += self.state.x
            vertex.y += self.state.y
        return vertices

    def apply_to_vertex(self, vertex):
        return Vector(vertex.x + self.state.x, vertex.y + self.state.y)


    #this updates sprites
    def update(self, target):
        self.state = self.functionality(target.rect)

    #this updates rects
    def update_rect(self, target):
        self.state = self.functionality((target.x, target.y))


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
