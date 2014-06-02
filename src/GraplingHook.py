import pygame
import math
from pygame.math import Vector2 as Vector
import sys
from Pendulum import Pendulum



pygame.init()
screen = pygame.display.set_mode((1000, 500))
clock = pygame.time.Clock()

class GraplingHook(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((60, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
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
    
    def calculate_angle(self):
        self.angle = self.rope.angle_to(self.limit)
        #print(self.angle, "YEAH")
        self.bob = Pendulum(90 - self.angle, self.distance_limit, (self.hook.x, self.hook.y))
        
    def retract(self):
        screen.fill((255, 255, 255))
        if self.distance > self.distance_limit:
            self.rect = self.rect.move([self.rope.x * 15, self.rope.y * 15])
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
        self.bob.recompute_angle()
        self.step = self.bob.dtheta
        self.rope.rotate_ip(self.step)
        self.rect.center = self.bob.rect.center


    def functionality(self, event):
        if event.type == pygame.MOUSEMOTION and self.should_aim:
                screen.fill((255, 255, 255))
                self.aim = pygame.mouse.get_pos()
                self.draw()
            
        if event.type == pygame.MOUSEBUTTONUP and self.should_aim:
            self.should_aim = False
            self.draw()
            self.should_retract = True
            self.calculate_rope()
            self.calculate_angle()
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL:
                self.should_release = True
                self.should_retract = False
                
    def release(self):
        screen.fill((255, 255, 255))
        self.calculate_rope()
        self.rect = self.rect.move([-self.rope.x * 8 - (math.sin(self.bob.theta) * int(self.bob.dtheta)),
                                    -self.rope.y * 10 + self.rope.y * (15 - self.time)])
        self.time += 0.7
    
    def draw(self):
        if self.should_retract:
            self.retract()
        pygame.draw.line(screen, (0, 255, 0), self.rect.center, self.aim)
        if self.should_release:
            self.release()
        
        
graple = GraplingHook(100, 450)  
graple.x = 50
graple.y = 20
#should_retract = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        graple.functionality(event)
    graple.draw()
    screen.blit(graple.image, graple.rect)
    
    pygame.display.update()
    clock.tick(60)