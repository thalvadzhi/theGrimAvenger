import math
import sys
import pygame
import Camera
import Environment
from pygame.math import Vector2 as Vector


pygame.init()

screen = pygame.display.set_mode((1000, 500))

clock = pygame.time.Clock()

class Batarang(pygame.sprite.Sprite):
    def __init__(self, x, y):
        #x and y are the coordinates of player's hand
        pygame.sprite.Sprite.__init__(self)
        self.imageMaster = pygame.image.load("batarang.png").convert_alpha()
        self.imageMaster = pygame.transform.scale(self.imageMaster, (60, 30))
        self.image = self.imageMaster
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
        oldCenter = self.rect.center
        self.image = pygame.transform.rotate(self.imageMaster, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter
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

    def draw(self, surface):
        # for event in pygame.event.get():
        #     if event.type == pygame.MOUSEBUTTONUP:
        #         mouse_position = pygame.mouse.get_pos()
        #         self.direct(mouse_position[0], mouse_position[1])
        #         self.should_fly = True
        surface.blit(self.image, self.rect)
        if self.should_fly:
            self.move()
            self.rotate()

        
# x = Environment.Block((255, 0, 123), 32, 32, 20, 20)

# color = (255, 0, 0)
# camera = Camera.Camera(2000, 500, 1000, 500)
# run = False
# a = Batarang(0, 450)
# allSprites = pygame.sprite.Group(a)
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             sys.exit()
#         if event.type == pygame.MOUSEBUTTONUP:
#             mouse_position = pygame.mouse.get_pos()
#             a.direct(mouse_position[0], mouse_position[1])
#             #print("YEAH")
#             run = True
#     camera.update(a)
#     screen.fill((255, 255, 255))
#     if a.rect.colliderect(x):
#         color = (0, 255, 0)
#     pygame.draw.rect(screen, color, camera.apply(x))
#     screen.blit(a.image, camera.apply(a))
#     keys = pygame.key.get_pressed()
#     if run:
#         a.move()
#         #a.rotate()
#     pygame.display.update()
#     clock.tick(60)
#
#
