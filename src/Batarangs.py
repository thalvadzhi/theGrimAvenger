import math
import sys
import pygame
import Camera
import Environment
from pygame.math import Vector2 as Vector


class Batarang(pygame.sprite.Sprite):
    def __init__(self, x, y):
        #x and y are the coordinates of player's hand
        pygame.sprite.Sprite.__init__(self)
        self.image_master = pygame.image.load("batarang.png").convert_alpha()
        self.image_master = pygame.transform.scale(self.image_master, (60, 30))
        self.image = self.image_master
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.rotation = 0
        self.gravity = 0
        self.frames = 0
        self.step = 40
        self.x = x
        self.y = y
        self.should_fly = False
        
    def rotate(self):
        old_center = self.rect.center
        self.image = pygame.transform.rotate(self.image_master, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        self.rotation += self.step
        if self.rotation > 360:
            self.rotation = self.step
        if self.frames >= 25:
            self.step -= 0.7
        
    def move(self):
        self.frames += 1
        #after some time gravity starts to take effect
        if self.frames >= 25:
            self.gravity += 0.4
        self.rect = self.rect.move([self.direction.x * 20, self.direction.y * 20 + self.gravity])
        self.rotate()
        
    
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

    def draw(self, surface, camera):
        surface.blit(self.image, camera.apply_to_rect(self.rect))
        if self.should_fly:
            self.move()
            self.rotate()

        
