import pygame
import math
from pygame.math import Vector2 as Vector
import sys
from Pendulum import Pendulum
from BasicShapes import Rectangle
from math import *


pygame.init()
screen = pygame.display.set_mode((1000, 500))
clock = pygame.time.Clock()

class GraplingHook():
    def __init__(self, x, y):
        self.image_master = pygame.image.load("graplinghook.png").convert_alpha()
        self.image_master = pygame.transform.scale(self.image_master, (80, 40))
        self.image = self.image_master

        self.hook_image_master = pygame.image.load("hook.png").convert_alpha()
        self.hook_image_master = pygame.transform.scale(self.hook_image_master, (40, 40))
        self.hook_image = self.hook_image_master

        self.hook_rect = Rectangle.get_rect(self.hook_image, (x, y))
        self.rect = Rectangle.get_rect(self.image, (x, y))

        self.hooker = Vector((self.hook_rect.x, self.hook_rect.y))

        self.aim = (x, y + 20)
        self.should_aim = True
        self.should_retract = False
        self.limit = Vector(1, 0)
        self.angle = 0
        self.rotation = 0
        self.step = 0
        self.should_release = False
        self.time = 0
        self.distance_limit = 150
        self.x = self.rect.x
        self.y = self.rect.y
        self.current_time = 0
        self.last_time = 0
        self.shooter = False
    
    def calculate_angle(self):
        self.angle = self.rope.angle_to(self.limit)
        self.bob = Pendulum(90 - self.angle, self.distance_limit, (self.hook.x, self.hook.y))
        
    def retract(self, timer):
        if self.distance > self.distance_limit:
            self.rect.advance(self.rope.x * 700 * (timer / 1000), self.rope.y * 700 * (timer / 1000))
            self.x += self.rope.x * 700 * (timer / 1000)
            self.y += self.rope.y * 700 * (timer / 1000)
            self.calculate_rope()
        else:
            self.swing()
    
    def calculate_rope(self):
        self.hook = Vector(self.aim)
        self.player = Vector(self.rect.center[0], self.rect.center[1])
        self.distance = self.hook.distance_to(self.player)
        self.rope = self.hook - self.player
        self.rope = self.rope.normalize()


    def swing(self):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.last_time >= 17:
            self.bob.recompute_angle()
            self.step = self.bob.dtheta
            self.rope = self.rope.rotate(self.step)
            self.rect = Rectangle.get_rect(self.image, self.bob.rect.center)
            self.x = self.rect.x
            self.y = self.rect.y

            self.last_time = self.current_time

    def shoot(self, timer):
        distance = sqrt((self.hook_rect.center[0] - self.aim[0]) ** 2 + (self.hook_rect.center[1] - self.aim[1]) ** 2)
        if int(distance) > 3:
            self.hook_rect.advance(self.rope.x * 700 * (timer / 1000), self.rope.y * 700 * (timer / 1000))
            self.hooker = Vector((self.hook_rect.x, self.hook_rect.y))
            print(distance)
        else:
            self.shooter = False

    def update(self, screen, timer):
        angle = Vector(self.aim) - Vector(self.rect.center)
        ang = angle.normalize()
        self.image = pygame.transform.rotate(self.image_master, angle.angle_to(Vector(1, 0)))
        self.hook_image = pygame.transform.rotate(self.hook_image_master, angle.angle_to(Vector(1, 0)))
        self.rect = Rectangle.get_rect(self.image, self.rect.center)

        self.x = self.rect.x
        self.y = self.rect.y
        if self.shooter:
            self.shoot(timer)
        elif not self.should_retract:
            #60 is the average of the widths of the two images
            self.hook_rect = Rectangle.get_rect(self.hook_image, (self.rect.center[0] + ang.x * 60, self.rect.center[1] + ang.y * 60))
        if self.should_retract and not self.shooter:
            self.retract(timer)
        if self.should_release:
            self.release(timer)
        self.draw(screen)

    def functionality(self, event, screen):
        if event.type == pygame.MOUSEMOTION and self.should_aim:
                self.aim = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONUP and self.should_aim:
            self.should_aim = False
            self.should_retract = True
            self.shooter = True
            self.calculate_rope()
            self.calculate_angle()
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL:
                self.should_release = True
                self.should_retract = False
                
    def release(self, timer):
        self.calculate_rope()

        self.rect.advance((- self.rope.x * 10 - (math.sin(self.bob.theta) * int(self.bob.dtheta))) * 15 * (timer / 1000),
                       (- self.rope.y * 10 + self.rope.y * (30 - self.time)) * 15 * (timer / 1000))
        self.time += 0.8
    
    def draw(self, screen):
        pygame.draw.line(screen, (0, 255, 0), self.rect.center, self.aim)
        screen.blit(self.image, (self.x, self.y))
        screen.blit(self.hook_image, (self.hook_rect.x, self.hook_rect.y))

graple = GraplingHook(100, 450)

#should_retract = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        graple.functionality(event, screen)

    time = clock.tick(120)

    screen.fill((255, 255, 255))
    graple.update(screen, time)
    graple.draw(screen)


    pygame.display.update()
