# This is just basic template just to find out what is needed for the ragdoll
# This will be split into multiple modules and files

import sys
import pygame

import VectorMath

from pygame.math import Vector2 as Vector


class Joint:

    def __init__(self, position_m):
        self.position_m = Vector(position_m)


class SolidConnection:

    def __init__(self, length_m, end_1, end_2):
        self.length_m = length_m  # this should not change
        self.end_1 = end_1  # those are intergers
        self.end_2 = end_2


class BetaBody:

    def __init__(self):
        self.joints = []
        self.levers = []

    def update_connections(self):
        self.connections = {_: [] for _ in range(len(self.joints))}
        for index, lever in enumerate(self.levers):
            self.connections[lever.end_1].append(index)
            self.connections[lever.end_2].append(index)

    def calculate_lengths(self, static):
        used_connections = set()

        def recursive_calculation(static):
            for connection in self.connections[static]:
                if connection not in used_connections:
                    used_connections.add(static)
                    if connection.end_1 != static:
                        self.joints[connection.end_1] = seperate_point(
                            self.joints[static].position_m,
                            self.joints[connection.end1].position_m,
                            connection.length_m)

                        recursive_calculation(connection.end_2)
                    else:
                        self.joints[connection.end_1] = seperate_point(
                            self.joints[static].position_m,
                            self.joints[connection.end1].position_m,
                            connection.length_m)

                        recursive_calculation(connection.end_1)

        recursive_calculation(static)

pygame.init()

screen = pygame.display.set_mode((500, 500))

clock = pygame.time.Clock()

while True:

    screen.fill((55, 155, 255))
    pygame.display.update()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
