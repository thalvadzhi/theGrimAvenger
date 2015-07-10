import math
import pygame
from constants import BOB_ANGLE, ROPE_WIDTH, SWINGING_LIGHT_RADIUS
from light import Light
from pendulum import Pendulum


class SwingingLight:
    def __init__(self, x, y, rope_length, obstacles=[]):
        """expects that set_up_surface for Light has been called"""
        self.x = x
        self.y = y
        self.obstacles = obstacles
        self.rope_length = rope_length
        self.bob = Pendulum(BOB_ANGLE, self.rope_length, (self.x, self.y))
        self.light = Light(self.x, self.y + self.rope_length,
                           SWINGING_LIGHT_RADIUS, self.obstacles)
        self.light.update()

    def update(self):
        self.bob.recompute_angle()
        x = self.bob.rect.center[0]
        y = self.bob.rect.center[1]
        self.light.update_light_position(x, y)

    def update_position(self, x, y):
        self.x = x
        self.y = y
        self.bob = Pendulum(BOB_ANGLE, self.rope_length, (self.x, self.y))
        self.light.update_light_position(self.x, self.y + self.rope_length)

    def update_obstacles(self, obstacles):
        self.obstacles = obstacles
        self.light.update_obstacles(self.obstacles)

    def collide(self, position):
        return math.sqrt((self.x - position[0]) ** 2 +
                         (self.y - position[1]) ** 2) <= 30

    def draw(self, surface, camera):
        pygame.draw.line(surface, (0, 0, 0), camera.apply((self.x, self.y)),
                         camera.apply((self.bob.rect.center[0],
                                       self.bob.rect.center[1])), 5)
        self.light.draw_light(camera)
        self.light.draw_shadow(camera)
