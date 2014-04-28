import math
import sys
import pygame

from VectorMath import seperate_point

from pygame.math import Vector2 as Vector

from _collections import defaultdict

pygame.init()

screen = pygame.display.set_mode((500, 500))

clock = pygame.time.Clock()



class Joint:

    def __init__(self, position_m):
        self.position_m = Vector(position_m)

    def __eq__(self, other):
        return self.position_m == other.position_m

    def __ne__(self, other):
        return self.position_m != other.position_m


class SolidConnection:

    def __init__(self, length_m, end_1, end_2):
        # this should not change
        self.length_m = math.ceil(length_m * 100) / 100
        self.end_1 = end_1  # those are intergers
        self.end_2 = end_2


class BetaBody:

    def __init__(self):
        self.joints = []
        self.levers = []
        self.fixes = 0

    def update_connections(self):
        self.connections = defaultdict(list)
        for index, lever in enumerate(self.levers):
            self.connections[lever.end_1].append(index)
            self.connections[lever.end_2].append(index)

    def fix_lengths(self, static):
        self.fixes += 1
        if self.fixes % len(self.connections) * 2 == 0:
             return
        for connection in self.connections[static]:
            connection = self.levers[connection]
            if connection.end_1 != static:
                new_joint = Joint(seperate_point(
                    self.joints[static].position_m,
                    self.joints[connection.end_1].position_m,
                    connection.length_m))
                if new_joint != self.joints[connection.end_1]:
                    self.joints[connection.end_1] = new_joint
                    self.fix_lengths(connection.end_1)
            else:
                new_joint = Joint(seperate_point(
                    self.joints[static].position_m,
                    self.joints[connection.end_2].position_m,
                    connection.length_m))
                if new_joint != self.joints[connection.end_2]:
                    self.joints[connection.end_2] = new_joint
                    self.fix_lengths(connection.end_2)

    def move_joint(self, joint, position_m):
        self.fixes = 0
        self.joints[joint].position_m = position_m
        self.fix_lengths(joint)

    def draw(self):
        for lever in self.levers:
            pygame.draw.line(screen, (0, 0, 0),
                             self.joints[lever.end_1].position_m,
                             self.joints[lever.end_2].position_m, 4)


mini_ragdoll = BetaBody()

joints = [Joint((50, 50)), Joint((60, 60)), Joint((10, 60)), Joint((70, 0))]

levers = [SolidConnection(70, 0, 1), SolidConnection(70, 1, 2),
          SolidConnection(70, 2, 3), SolidConnection(70, 0, 3)]


mini_ragdoll.joints = joints
mini_ragdoll.levers = levers
mini_ragdoll.update_connections()
mini_ragdoll.fix_lengths(0)

new_positions = [70, 0]

while True:
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        new_positions[0] -= 1
        mini_ragdoll.move_joint(2, (new_positions[0], new_positions[1]))
        screen.fill((55, 155, 255))
        mini_ragdoll.draw()

    elif keys[pygame.K_RIGHT]:
        new_positions[0] += 1
        mini_ragdoll.move_joint(2, (new_positions[0], new_positions[1]))
        screen.fill((55, 155, 255))
        mini_ragdoll.draw()

    elif keys[pygame.K_UP]:
        new_positions[1] -= 1
        mini_ragdoll.move_joint(2, (new_positions[0], new_positions[1]))
        screen.fill((55, 155, 255))
        mini_ragdoll.draw()

    elif keys[pygame.K_DOWN]:
        new_positions[1] += 1
        mini_ragdoll.move_joint(2, (new_positions[0], new_positions[1]))
        screen.fill((55, 155, 255))
        mini_ragdoll.draw()

    else:
        screen.fill((55, 155, 255))
        mini_ragdoll.draw()

    # pygame.draw.polygon(screen, (255, 255, 255),
    #                    [(0, 0), (0, 50), (50, 50), (50, 0)])
    pygame.display.update()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()