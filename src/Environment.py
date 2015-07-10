import pygame
from pygame import *
import pygame.gfxdraw
from pygame.math import Vector2 as Vector
import math
from Camera import Camera
from Pendulum import Pendulum
from BasicShapes import Rectangle, Circle
from light_cast_v3 import Point, Line
from pixelperfect import get_hitmask
from Constants import TAG_GROUND, BOB_ANGLE, SWINGING_LIGHT_RADIUS, ROPE_WIDTH


class Block():
    def __init__(self, colour, width, height, x, y, tag=TAG_GROUND):
        self.image = pygame.Surface((width, height))
        self.image.fill(colour)
        self.width = width
        self.x = x
        self.y = y
        self.height = height
        self.tag = tag
        self.walls = []
        self.rect = Rectangle(width, height,
                              Vector(x + width / 2, y + height / 2))
        self.hitmask = get_hitmask(self.rect, self.image, 0)
        self.image = 0
        self.colour = colour
        self.generate_walls()

    def generate_walls(self):
        points = []
        for vertex in self.rect.vertices:
            points.append(Point(vertex.x, vertex.y))
        index = 0
        while index < len(points) - 1:
            point1 = points[index]
            point2 = points[index + 1]
            self.walls.append(Line(point1, point2))
            index += 1
        self.walls.append(Line(points[0], points[3]))

    def draw(self, screen, camera=0):
        self.rect.draw(screen, self.colour, camera)

    def load_texture(self, name=0):
        if name != 0:
            self.image = pygame.image.load(name).convert_alpha()
            self.image = pygame.transform.scale(self.image,
                                                (self.width, self.height))
        else:
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(self.colour)


class SawBlock():
    def __init__(self, x, y, length):
        ''' x and y should be the coordinates of the pivot '''
        self.rope_width = 10
        self.rope_height = length
        self.saw_image_master = pygame.image.load("../ArtWork/Environment/saw.png").convert_alpha()
        self.saw_image_master = pygame.transform.scale(self.saw_image_master,
                                                       (50, 50))
        self.image = self.saw_image_master

        self.rect_center = Vector(x, y + self.rope_height + 15)
        self.rect = Rectangle.get_rect(self.image, self.rect_center)
        self.collision_circle = Circle(25, self.rect_center) 
        self.x = x
        self.y = y

        self.step = 40
        self.swing_step = 1
        self.rotation = 0
        self.is_severed = False
        self.angle = 45
        self.bob = Pendulum(self.angle, self.rope_height, (self.x, self.y))
        self.time = 0
        self.tick_time = 0
        self.entrances = 0
        self.last_time = 0
        self.current_time = 0

    def rotate_saw(self, time):
        self.image = pygame.transform.rotate(self.saw_image_master,
                                             self.rotation)
        self.rect = Rectangle.get_rect(self.image, self.rect_center)
        self.rotation += 300 * time / 1000
        if self.rotation > 360:
            self.rotation = self.step

    def swing_rope(self):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.last_time >= 17:
            self.bob.recompute_angle()
            self.rect_center = self.bob.rect.center
            self.rect.center = self.rect_center
            self.collision_circle.move(
                    self.rect_center - self.collision_circle.position)
            self.last_time = self.current_time

    def deploy(self):
        self.is_severed = True

        self.direction = Vector((self.x, self.y)) - Vector(self.rect_center[0],
                                                           self.rect_center[1])
        self.direction = self.direction.normalize()

        #pseudo velocity vector - defines only direction not speed
        self.velocity = self.direction.rotate(-90 * self.sign(self.bob.dtheta))
        self.velocity = self.velocity.normalize()

    def sign(self, number):
        if number == 0:
            return
        if number > 0:
            return 1
        else:
            return -1

    def load_texture(self, name):
        self.saw_image_master = pygame.image.load(name).convert_alpha()
        self.saw_image_master = pygame.transform.scale(self.saw_image_master,
                                                       (50, 50))
        self.image = self.saw_image_master

    def update(self, time):
        if self.is_severed:
            self.time += 0.5

            self.rect.advance((self.velocity.x * 10 +
                               math.sin(math.fabs(self.bob.theta))),
                              (self.velocity.y * 8 * Vector(0, 1).x * 10 +
                               self.time))
            self.rect_center = self.rect.center
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

    def collide_line(self, point_x, point_y):
        #y = kx + c
        if point_y > self.rect.center[1] or point_y < self.y:
            return False
        if int(self.rect.center[0]) - self.x != 0:
            k = (self.rect.center[1] - self.y) / (self.rect.center[0] - self.x)
            c = self.y - k * self.x
        else:
            return point_x in range(self.x - 10, self.x + 10) \
                and point_y in range(self.y, self.rect.center[1])

        #add room for error due to batarangs teleportational tendencies
        for i in range(0, 10):
            if int(point_y) == int(k * point_x + c) - i or \
                    int(point_y) == int(k * point_x + c) + i:
                return True
        return False


    def collide(self, bat):
        #implement list of bats
        if self.collide_line(bat.rect.x, bat.rect.y) and not self.is_severed:
            self.deploy()


