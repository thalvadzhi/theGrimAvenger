from pygame import image, transform
import pygame.gfxdraw
import math
from pygame.math import Vector2 as Vector
from Pendulum import Pendulum
from BasicShapes import Rectangle, Circle
from Constants import TAG_GROUND, SAW_IMAGE, SAW_DIMENSION, TICKS_FOR_60_FPS,\
    SAW_ROPE_ANGLE, ROTATION_STEP, SAW_ROPE_WIDTH


class Block():
    def __init__(self, colour, width, height, x, y, tag=TAG_GROUND):
        self.width, self.height = width, height
        self.x, self.y = x, y
        self.tag = tag
        self.colour = colour
        self.rect = Rectangle(width, height,
                              Vector(x + width / 2, y + height / 2))

    def draw(self, screen, camera=0):
        self.rect.draw(screen, self.colour, camera)


class SawBlock():
    def __init__(self, x, y, length):
        """ x and y should be the coordinates of the pivot """
        self.rope_height = length
        self.x, self.y = x, y
        self.rope_width = SAW_ROPE_WIDTH

        self.saw_image_master = image.load("../ArtWork/Environment/{0}"
                                           .format(SAW_IMAGE)).convert_alpha()
        self.saw_image_master = transform.scale(self.saw_image_master,
                                                SAW_DIMENSION)
        self.image = self.saw_image_master

        self.center_old = Vector(x, y + self.rope_height + 15)
        self.rect = Rectangle.get_rect(self.image, self.center_old)
        self.collision_circle = Circle(25, self.center_old)

        self.step = ROTATION_STEP
        self.rotation = 0
        self.time = 0
        self.last_time = 0
        self.current_time = 0
        self.direction = Vector((0, 0))
        self.velocity = Vector((0, 0))
        self.bob = Pendulum(SAW_ROPE_ANGLE, self.rope_height, (self.x, self.y))
        self.is_severed = False

    def rotate_saw(self, time):
        self.image = pygame.transform.rotate(self.saw_image_master,
                                             self.rotation)
        self.rect = Rectangle.get_rect(self.image, self.center_old)
        self.rotation += 300 * time / 1000
        if self.rotation > 360:
            self.rotation = self.step

    def swing_rope(self):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.last_time >= TICKS_FOR_60_FPS:
            self.bob.recompute_angle()
            self.center_old = self.bob.rect.center
            self.rect.center = self.center_old
            self.collision_circle.move(
                self.center_old - self.collision_circle.position)
            self.last_time = self.current_time

    def deploy(self):
        self.is_severed = True

        self.direction = Vector((self.x, self.y)) - Vector(self.center_old)
        self.direction = self.direction.normalize()

        # pseudo velocity vector - defines only direction not speed
        self.velocity = self.direction.rotate(-90 * self.sign(self.bob.d_theta))
        self.velocity = self.velocity.normalize()

    def sign(self, number):
        if number >= 0:
            return 1
        else:
            return -1

    def update(self, time):
        if self.is_severed:
            self.time += 0.5

            self.rect.advance((self.velocity.x * 10 +
                               math.sin(math.fabs(self.bob.theta))),
                              (self.velocity.y * 8 * Vector(0, 1).x * 10 +
                               self.time))
            self.center_old = self.rect.center
        else:
            self.rotate_saw(time)
            self.swing_rope()

    def draw(self, surface, camera):
        if self.is_severed:
            surface.blit(self.image, camera.apply((self.rect.x, self.rect.y)))

        else:
            surface.blit(self.image, camera.apply((self.rect.x, self.rect.y)))
            pygame.draw.line(surface, (0, 0, 0),
                             camera.apply((self.x, self.y)),
                             camera.apply((self.rect.center[0],
                                           self.rect.center[1])),
                             self.rope_width)
