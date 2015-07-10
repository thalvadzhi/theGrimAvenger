import pygame
from pygame.math import Vector2 as Vector
import sys
from BasicShapes import Rectangle, Triangle
from Camera import Camera
from Constants import BLOCK_SIZE
from Environment import Block
from pixelperfect import get_hitmask, collide
from light_cast_v3 import Line, Point


class Batarang():
    def __init__(self, x, y, world):
        #x and y are the coordinates of player's hand
        self.width = 35
        self.height = 15
        self.image_master = pygame.image.load("batarang2.png").convert_alpha()
        self.image_master = pygame.transform.scale(self.image_master,
                                                   (self.width, self.height))
        self.world = world

        self.image = self.image_master
        self.rect_center = (x, y)
        self.rect = Rectangle.get_rect(self.image, self.rect_center)
        self.hitmask = get_hitmask(self.rect, self.image, 0)
        #coordinates of topleft vertex
        self.x = x - self.width // 2
        self.y = y - self.height // 2
        self.triangle = Triangle([Vector(self.x, self.y), Vector(self.x + self.width, self.y), Vector(self.x + self.width // 2, self.y + self.height)], self.rect_center)
        self.triangle.load_avatar("/Environment/batarang2.png")
        self.triangle.scale_avatar(self.width, self.height)
        self.direction = Vector(0, 0)
        self.rotation = 0
        self.gravity = 0
        self.frames = 0
        self.step = 40
        self.speed = 0
        self.should_fly = False

    def rotate(self, timer):
        self.image = pygame.transform.rotate(self.image_master,
                                             self.rotation * (1000 / timer))
        self.rect = Rectangle.get_rect(self.image, self.rect.center)

        self.hitmask = get_hitmask(self.rect, self.image, 0)
        self.triangle.rotate(self.rotation * (1000 / timer))
        self.triangle.move(self.rect.center - self.triangle.position)
        self.rotation += self.step
        if self.rotation > 360:
            self.rotation = self.step

    def move(self, timer):
        self.speed = 50 * 10 * (timer / 1000)
        self.x += self.direction.x * self.speed
        self.y += self.direction.y * self.speed

        self.triangle.move(self.direction * self.speed)
        old_center = self.rect_center
        self.rect_center = (old_center[0] + self.direction.x * self.speed,
                            old_center[1] + self.direction.y * self.speed)
        self.rect.center = self.rect_center
        self.rect.center = (self.x + self.rect.width / 2,
                            self.y + self.rect.height / 2)
        self.hitmask = get_hitmask(self.rect, self.image, 0)

    def get_next_position(self):
        return self.x + self.direction.x * self.speed, self.y + self.direction.y * self.speed

    def direct(self, mouse_x, mouse_y):
        #get coordinates of player hand
        #get coordinates of mouse
        #run vector between the two to determine the direction of the batarang
        self.direction = Vector(mouse_x - self.x, mouse_y - self.y)
        self.direction = self.direction.normalize()

    def take_action(self, camera):
        self.mouse_position = camera.apply(pygame.mouse.get_pos())
        self.direct(self.mouse_position[0], self.mouse_position[1])
        self.should_fly = True
        self.last_update = pygame.time.get_ticks()

    def update(self):
        timer = pygame.time.get_ticks() - self.last_update + 1
        self.last_update += timer
        if self.should_fly:
            self.move(timer)
            self.rotate(timer)
            self.collides(self.world)
        self.hitmask = get_hitmask(self.rect, self.image, 0)
        return self.should_fly

    def draw(self, surface, camera=0):
        if camera != 0:
            self.triangle.display_avatar(surface, camera)
        else:
            surface.blit(self.image, (self.x, self.y))

    def collides(self, world):
        next_position = self.get_next_position()

        collision_line = Line(Point(self.x, self.y), Point(next_position[0], next_position[1]))
        for obstacle in world:
            if self.triangle.check_if_collide(obstacle.rect)[0]:
                self.should_fly = False
                break
            for line in obstacle.walls:
                intersection = Line.get_intersection(line, collision_line)
                if intersection is not None:

                    while not self.triangle.check_if_collide(obstacle.rect)[0]:
                        self.x += self.direction.x
                        self.y += self.direction.y
                        self.rect.center = Vector((self.x, self.y))
                        self.triangle.move(self.direction * 2)
                    self.should_fly = False

    def reposition(self, coordinates, orientation, direction=None):
        self.rect.center = Vector(coordinates)
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.triangle.move(self.rect.center - self.triangle.position)
        self.triangle.direction = orientation.normalize()
        if direction is None:
            self.rotation = 0
        else:
            self.rotation = direction.angle_to(Vector(1, 0))
        self.image = pygame.transform.rotate(self.image_master,
                                             self.rotation)
        self.rect = Rectangle.get_rect(self.image, self.rect.center)

        #self.hitmask = get_hitmask(self.rect, self.image, 0)
