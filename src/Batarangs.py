import math
import sys
import pygame
import Camera
#import Environment
from pygame.math import Vector2 as Vector
from BasicShapes import Rectangle
from pixelperfect import get_hitmask

class Batarang():
    def __init__(self, x, y):
        #x and y are the coordinates of player's hand
        self.width = 60
        self.height = 30
        self.image_master = pygame.image.load("batarang.png").convert_alpha()
        self.image_master = pygame.transform.scale(self.image_master, (self.width, self.height))
        self.image = self.image_master
        self.rect_center = (x, y)
        self.rect = Rectangle.get_rect(self.image, self.rect_center)

        #coordinates of topleft vertex
        self.x = x - self.width // 2
        self.y = y - self.height // 2

        self.mask = get_hitmask(self, 0)

        self.rotation = 0
        self.gravity = 0
        self.frames = 0
        self.step = 40
        self.should_fly = False


    def rotate(self, timer):
        self.image = pygame.transform.rotate(self.image_master, self.rotation * (1000 / timer))
        self.rect = Rectangle.get_rect(self.image, self.rect_center)
        self.mask = get_hitmask(self, 0)
        self.rotation += self.step
        if self.rotation > 360:
            self.rotation = self.step
        if self.frames >= 25:
            self.step -= 0.7


    def move(self, timer):
        #IMPLEMENT GRAVITY
        speed = 25 * 60 * (timer / 1000)
        self.x += self.direction.x * speed
        self.y += self.direction.y * speed

        old_center = self.rect_center

        self.rect_center = (old_center[0] + self.direction.x * speed, old_center[1] + self.direction.y * speed)

        self.rotate(timer)
        
    
    def direct(self, mouse_x, mouse_y):
        #get coordinates of player hand
        #get coordinates of mouse
        #run vector between the two to determine the direction of the batarang
        self.direction = Vector(mouse_x - self.x, mouse_y - self.y)
        self.direction = self.direction.normalize()

    def control(self):
        mouse_position = pygame.mouse.get_pos()
        self.direct(mouse_position[0], mouse_position[1])
        self.should_fly = True

    def update(self, timer):
        if self.should_fly:
            self.move(timer)
            self.rotate(timer)

    def draw(self, surface, camera):
        #to be moved in Render module
        surface.blit(self.image, camera.apply_to_tuple((self.x, self.y)))
        self.rect.draw(surface)
        
