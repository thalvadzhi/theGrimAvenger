import pygame
import math
from pygame.math import Vector2 as Vector
import sys

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
        self.step = -2
        self.should_release = False
        self.time = 0;
    
    def calculate_angle(self):
        self.angle = self.rope.angle_to(self.limit)
        
    def retract(self):
        screen.fill((255, 255, 255))
        if self.distance > 150:
            self.rect = self.rect.move([self.rope.x * 15, self.rope.y * 15])
            self.calculate()
        else:
            self.swing()
    
    def calculate(self):
        self.hook = Vector(self.aim)
        self.player = Vector(self.rect.center[0], self.rect.center[1])
        self.distance = self.hook.distance_to(self.player)
        self.rope = self.hook - self.player
        self.rope = self.rope.normalize()
        
    
    def swing(self):
        #swing the player also reduce the angle of swinging with time
        self.time += 1
        # self.rotation += math.fabs(self.step)
        # if self.rotation >= 180 - 2 * self.angle:
        #     self.step *= -1
        #     self.rotation = 0
        #     #self.angle += 3
        #     if 180 - 2 * self.angle <= 0:
        #         self.step = 0
        self.player = self.hook - (self.rope * self.distance)
#        angle_to_Oy = - (270 - (-self.rope).angle_to(Vector(0, 1)))
        angle_to_Oy = ((-self.rope).angle_to(Vector(0, -1)) - 90)

        self.step = (angle_to_Oy) - (90 - self.angle) * math.cos(math.sqrt(0.001) * (self.time))

        self.rect.center = [self.player.x, self.player.y]
        print(self.step, angle_to_Oy)
        self.rope.rotate_ip(self.step)
        
    
    def functionality(self, event):
        if event.type == pygame.MOUSEMOTION and self.should_aim:
                screen.fill((255, 255, 255))
                self.aim = pygame.mouse.get_pos()
                self.draw()
            
        if event.type == pygame.MOUSEBUTTONUP and self.should_aim:
            self.should_aim = False
            self.draw()
            self.should_retract = True
            self.calculate()
            self.calculate_angle()
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL:
                self.should_release = True
                self.should_retract = False
                
    def release(self):
        screen.fill((255, 255, 255))
        self.rect = self.rect.move([-self.rope.x*10, -self.rope.y*10])
    
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
    clock.tick(10)