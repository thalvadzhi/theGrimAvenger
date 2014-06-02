import pygame, sys
from pygame.locals import *
from math import sin, cos, radians

class BobMass(pygame.sprite.Sprite):
    def __init__(self, angle, swing_length, pivot):
        pygame.sprite.Sprite.__init__(self)
        self.theta = angle
        self.dtheta = 0
        self.swing_length = swing_length
        self.pivot = pivot
        self.time = 0
        self.rect = pygame.Rect(self.pivot[0]-self.swing_length*cos(radians(self.theta)),
                                self.pivot[1]+self.swing_length*sin(radians(self.theta)),
                                1, 1)

    def recompute_angle(self):
        self.time += 1
        #modulates gravity
        scaling = 2000.0 / (self.swing_length ** 2)

        firstDDtheta = -sin(radians(self.theta)) * scaling
        midDtheta = self.dtheta + firstDDtheta
        midtheta = self.theta + (self.dtheta + midDtheta) / 2.0

        midDDtheta = -sin(radians(midtheta)) * scaling
        midDtheta = self.dtheta + (firstDDtheta + midDDtheta) / 2
        midtheta = self.theta + (self.dtheta + midDtheta) / 2

        midDDtheta = -sin(radians(midtheta)) * scaling
        lastDtheta = midDtheta + midDDtheta
        lasttheta = midtheta + (midDtheta + lastDtheta) / 2.0

        lastDDtheta = -sin(radians(lasttheta)) * scaling
        lastDtheta = midDtheta + (midDDtheta + lastDDtheta) / 2.0
        lasttheta = midtheta + (midDtheta + lastDtheta) / 2.0

        self.dtheta = lastDtheta
        self.theta = lasttheta
        self.rect = pygame.Rect(self.pivot[0] -
                                self.swing_length * sin(radians(self.theta)),
                                self.pivot[1] +
                                self.swing_length * cos(radians(self.theta)), 1, 1)


