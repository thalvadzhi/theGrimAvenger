import pygame
import sys
import os
from pygame.math import Vector2 as Vector

from Joints import RailJoint

from Control import Control

from RagDoll import HumanRagdoll

from BasicShapes import *

pygame.init()

screen = pygame.display.set_mode((500, 500))

clock = pygame.time.Clock()

shapes = [Rectangle(100, 100, Vector((20, 20))),
          Rectangle(100, 100, Vector((200, 200)))]
shapes = [Triangle([130, 120, 110], Vector((20, 20))),
          Triangle([130, 120, 110], Vector((300, 300)))]
shapes = [Circle(100, Vector((20, 20))),
          Circle(100, Vector((300, 300)))]
shapes = [Rectangle(100, 100, Vector((20, 20))),
          Circle(100, Vector((300, 300)))]
shapes = [Triangle([130, 120, 110], Vector((20, 20))),
          Circle(100, Vector((300, 300)))]
#shapes = [Rectangle(100, 100, Vector((20, 20))),
#          Triangle([130, 120, 110], Vector((300, 300)))]

control = Control(2)

for shape in shapes:
    shape.pivot_m = Vector(0, 0)
    control.left_button_selectable.append(shape)

# rail = RailJoint(Vector(0, 250), Vector(500, 250))
# rail._bodies_positions[shapes[1]] = Vector(50, 50)
# shapes[1].joints.append(rail)
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
    collide = shapes[0].check_if_collide(shapes[1])
    if collide:
        shapes[1].move(collide)
    for shape in shapes:
        shape.draw(screen, colour)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    pygame.display.update()
    clock.tick(60)

    control.handle_user_input()
