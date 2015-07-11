from pygame.math import Vector2 as Vector
from basicshapes import Rectangle


class Camera:
    def __init__(self, width, height, window_width, window_height):
        self.state = Rectangle(width, height,
                               Vector(0 + width // 2, 0 + height // 2))
        self.half_width = window_width // 2
        self.half_height = window_height // 2
        self.window_width = window_width
        self.window_height = window_height

    def apply(self, target):
        if isinstance(target, tuple):
            result_x = target[0] + self.state.x
            result_y = target[1] + self.state.y
            return result_x, result_y
        elif isinstance(target, Vector):
            return Vector(target.x + self.state.x, target.y + self.state.y)
        elif isinstance(target, list):
            result = []
            for vertex in target:
                if isinstance(vertex, Vector):
                    result.append(Vector((vertex.x + self.state.x,
                                          vertex.y + self.state.y)))
                elif isinstance(vertex, tuple):
                    result.append((vertex[0] + self.state.x,
                                   vertex[1] + self.state.y))
                else:
                    raise TypeError
            return result

    def update(self, target):
        if isinstance(target, tuple):
            self.state = self.functionality(target)
        elif isinstance(target, Rectangle) or isinstance(target, Vector):
            self.state = self.functionality((target.x, target.y))

    def reverse_apply(self, target):
        if isinstance(target, tuple):
            result_x = target[0] - self.state.x
            result_y = target[1] - self.state.y
            return result_x, result_y
        elif isinstance(target, Vector):
            return Vector(target.x - self.state.x, target.y - self.state.y)
        elif isinstance(target, list):
            result = []
            for vertex in target:
                if isinstance(vertex, Vector):
                    result.append(Vector((vertex.x - self.state.x,
                                          vertex.y - self.state.y)))
                else:
                    raise TypeError
            return result

    def functionality(self, target):
        """defines how the camera will move,
        also makes sure it doesn't go outside level space
        """
        left, top = target[0], target[1]
        left = self.half_width - left
        top = self.half_height - top

        left = min(0, left)
        left = max((self.window_width - self.state.width), left)
        top = max((self.window_height - self.state.height), top)
        top = min(0, top)
        return Rectangle(self.state.width, self.state.height,
                         Vector(left + self.state.width // 2,
                                top + self.state.height // 2))
