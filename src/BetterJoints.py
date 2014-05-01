import math
import sys
import pygame

from VectorMath import seperate_point

from pygame.math import Vector2 as Vector

from collections import OrderedDict
from _collections import defaultdict

pygame.init()

screen = pygame.display.set_mode((500, 500))

clock = pygame.time.Clock()


class Joint:

    def __init__(self, position_m):
        self.position_m = position_m
        self.bodies = []

    def add_object(self, new_body):
        self.bodies.append(new_body)
        new_body.add_joint(self)


class Rectangle:

    def __init__(self, width_m, heigth_m, position_m):
        """
        position_m Is the position of the center of mass
        """
        self.width_m = width_m
        self.heigth_m = heigth_m
        self.position_m = Vector(position_m)
        self.joints = []

        self.diraction = Vector((1, 0))

    def rotate(self, rotation):
        self.diraction = self.diraction.rotate(rotation)
        self.joints = [(joint, position_on_body.rotate(rotation))
                       for joint, position_on_body in self.joints]

    def move(self, movement_m):
        self.position_m = self.position_m + movement_m
        for joint in self.joints:
            joint.update(self)

    def move_to_joint(self, joint):
        position_on_body = sum(
            [vec for _, vec in self.joints if _ is joint], Vector((0, 0)))
        new_position = joint.position_m - position_on_body
        translation = new_position - self.position_m
        if translation.x > 0.27 or translation.x < -0.27 or \
           translation.y > 0.27 or translation.y < -0.27:
            self.move(translation)

    def add_joint(self, new_joint):
        position_on_body = (new_joint.position_m - self.position_m) +\
            (Vector((1, 0)) - self.diraction)
        self.joints.append((new_joint, position_on_body))

    def draw(self):
        perpendicular = self.diraction.rotate(90)
        vertices = []
        vertices.append(perpendicular * self.heigth_m / 2 +
                        self.diraction * self.width_m / 2 + self.position_m)
        vertices.append(perpendicular * self.heigth_m / -2 +
                        self.diraction * self.width_m / 2 + self.position_m)
        vertices.append(perpendicular * self.heigth_m / -2 +
                        self.diraction * self.width_m / -2 + self.position_m)
        vertices.append(perpendicular * self.heigth_m / 2 +
                        self.diraction * self.width_m / -2 + self.position_m)

        pygame.draw.polygon(screen, (0, 0, 0), vertices)


class BallJoint (Joint):

    def move(self, movement_m):
        for body in self.bodies:
            pass  # Todo: add functionality

    def update(self, stationary):
        position_on_body = sum(
            [_ for joint, _ in stationary.joints if _ is self], Vector((0, 0)))
        self.position_m = position_on_body + stationary.position_m
        for body in self.bodies:
            if body is not stationary:
                body.move_to_joint(self)

rectangle = Rectangle(20, 50, Vector((250, 250)))
rectangles = [Rectangle(20, 50, Vector((23, 250))),
              Rectangle(20, 50, Vector((250, 23)))]

# joints = [Joint((50, 50)), Joint((60, 60)), Joint((10, 60)), Joint((70, 0))]

# levers = [SolidConnection(70, 0, 1), SolidConnection(70, 1, 2),
#          SolidConnection(70, 2, 3), SolidConnection(70, 0, 3)]


# mini_ragdoll.joints = joints
# mini_ragdoll.levers = levers
# mini_ragdoll.update_connections()
# mini_ragdoll.fix_lengths(0)


while True:
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        rectangle.move(Vector((-1, 0)))
        screen.fill((55, 155, 255))
        rectangle.draw()

    elif keys[pygame.K_RIGHT]:
        rectangle.move(Vector((1, 0)))
        screen.fill((55, 155, 255))
        rectangle.draw()

    elif keys[pygame.K_UP]:
        rectangle.rotate(1)
        screen.fill((55, 155, 255))
        rectangle.draw()

    elif keys[pygame.K_DOWN]:
        rectangle.rotate(-1)
        screen.fill((55, 155, 255))
        rectangle.draw()

    else:
        screen.fill((55, 155, 255))
        rectangle.draw()

    # pygame.draw.polygon(screen, (255, 255, 255),
    #                    [(0, 0), (0, 50), (50, 50), (50, 0)])
    pygame.display.update()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
#
# class BodyPart:
#
#     proportions = {"Forearm": 6.3, "Arm": 5.2, "Neck": 13, "Head": 8,
#                    "Torso": 2.2, "Thigh": 4, "Calf": 4.2}
#
#     def __init__(self, heigth_m, part, previous_joint):
#         self.upper_joint = previous
#         self.lower_joint = Joint(previous_joint + Vector(
#             0, heigth_m / BodyPart.proportions[part]))
#         self.length_m = FixedLengthConnection(
#             heigth_m / BodyPart.proportions, shoulder, self.elbow)
#
#
# class HumanRagdoll(FixedLengthJointSystem):
#
#     def __init__(self, heigth_m, position_m=Vector(0, 0)):
#         self.joints = {"Head": Joint(position_m)}
#         self.body_parts = {
#             "Head": BodyPart(heigth_m, "Head", self.joints["Head"])}
#         self.joints.append(self.body_parts["Head"].lower_joint)
#         self.body_parts["Neck"] = BodyPart(heigth_m, "Neck"
