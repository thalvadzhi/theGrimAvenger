import pygame

from pygame.math import Vector2 as Vector
from Batarangs import Batarang
from control import Control
from motions import Motion
from ragdoll import HumanRagdoll
from Camera import Camera
from basicshapes import *
from Environment import Block, SawBlock
from pixelperfect import collide as pixel
import sys

pygame.init()

screen = pygame.display.set_mode((1000, 1000))

clock = pygame.time.Clock()

cube1 = Rectangle(70, 70, Vector(250, 500))
cube2 = Triangle((70, 70, 70), Vector(250, 500))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        cube1.move(Vector((2, 0)))

    if keys[pygame.K_LEFT]:
        cube1.move(Vector((-2, 0)))

    if keys[pygame.K_UP]:
        cube1.move(Vector((0, -2)))

    if keys[pygame.K_DOWN]:
        cube1.move(Vector((0, 2)))

    collide = cube1.check_if_collide(cube2)
    if collide[0]:
        cube2.move(collide[1])

    screen.fill((55, 155, 255))
    cube1.draw(screen)
    cube2.draw(screen)

    pygame.display.update()
    timer = clock.tick(120)


    # control.handle_user_input()

