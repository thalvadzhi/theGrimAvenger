import pygame
import sys
import os
from pygame.math import Vector2 as Vector

from Control import Control

from RagDoll import HumanRagdoll

from BasicShapes import *

pygame.init()

screen = pygame.display.set_mode((500, 500))

clock = pygame.time.Clock()

shapes = [Circle(100, Vector((20, 20))),
          Triangle([130, 120, 110], Vector((100, 100)))]

while True:
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        shapes[0].move(Vector((-1, 0)))

    elif keys[pygame.K_RIGHT]:
        shapes[0].move(Vector((1, 0)))

    elif keys[pygame.K_UP]:
        shapes[0].move(Vector((0, -1)))

    elif keys[pygame.K_DOWN]:
        shapes[0].move(Vector((0, 1)))

    screen.fill((55, 155, 255))
    colour = (0, 0, 0)
    if shapes[0].check_if_collide(shapes[1]):
        colour = (255, 0, 0)
    for shape in shapes:
        shape.draw(screen, colour)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    pygame.display.update()
    clock.tick(60)
