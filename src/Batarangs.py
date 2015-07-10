import pygame
from pygame.math import Vector2 as Vector
import sys
from BasicShapes import Rectangle
from Camera import Camera
from Constants import BLOCK_SIZE
from Environment import Block
from pixelperfect import get_hitmask, collide
from light_cast_v3 import Line, Point


class Batarang():
    def __init__(self, x, y, world):
        #x and y are the coordinates of player's hand
        self.width = 25
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

        self.rotation += self.step
        if self.rotation > 360:
            self.rotation = self.step

    def move(self, timer):
        self.speed = 50 * 10 * (timer / 1000)
        self.x += self.direction.x * self.speed
        self.y += self.direction.y * self.speed

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

    def take_action(self):
        self.mouse_position = pygame.mouse.get_pos()
        self.direct(self.mouse_position[0], self.mouse_position[1])
        self.should_fly = True

    def update(self, timer):
        if self.should_fly:
            self.move(timer)
            self.rotate(timer)
        self.collide(self.world)
        self.hitmask = get_hitmask(self.rect, self.image, 0)

    def draw(self, surface, camera=0):
        if camera != 0:
            surface.blit(self.image, camera.apply((self.x, self.y)))

        else:
            surface.blit(self.image, (self.x, self.y))

    def collide(self, world):
        next_position = self.get_next_position()

        collision_line = Line(Point(self.x, self.y), Point(next_position[0], next_position[1]))
        for obstacle in world:

            for line in obstacle.walls:
                intersection = Line.get_intersection(line, collision_line)
                if intersection is not None:

                    # while not collide(self, obstacle):
                    #     print("YEAH")
                    #     amount = 2
                    #     self.x += self.direction.x * amount
                    #     self.y += self.direction.y * amount
                    #     old_center = self.rect_center
                    #
                    #     self.rect_center = (old_center[0] + self.direction.x * amount,
                    #                         old_center[1] + self.direction.y * amount)
                    #     self.rect.center = self.rect_center
                    #     self.rect = Rectangle.get_rect(self.image, self.rect.center)
                    #     self.hitmask = get_hitmask(self.rect, self.image, 0)
                    self.rect.center = Vector(intersection.x, intersection.y)
                    self.x = intersection.x
                    self.y = intersection.y
                    self.should_fly = False



    def reposition(self, coordinates, direction):
        self.rect.center = Vector(coordinates)
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.rotation = direction.angle_to(Vector(1, 0))
        self.image = pygame.transform.rotate(self.image_master,
                                             self.rotation)
        self.rect = Rectangle.get_rect(self.image, self.rect.center)

        self.hitmask = get_hitmask(self.rect, self.image, 0)



pygame.init()
screen = pygame.display.set_mode((800, 600))
timer = pygame.time.Clock()
x = [Block((0, 0, 0), 100, 100, 300, 100)]
b = Batarang(100, 400, x)
c = Camera(800, 600, 800, 600)
while True:

    mouse_position = pygame.mouse.get_pos()
    events = pygame.event.get()
    screen.fill((255, 255, 255))
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            b.take_action()
    b.draw(screen, c)
    x[0].draw(screen, c)
    z = timer.tick(60)
    b.update(z)
    pygame.display.update()
