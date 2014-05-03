import math
import sys
import pygame

from VectorMath import seperate_point
from Events import Events

from pygame.math import Vector2 as Vector

from collections import OrderedDict
from _collections import defaultdict

from BasicShapes import Rectangle

pygame.init()

screen = pygame.display.set_mode((500, 500))

clock = pygame.time.Clock()


class Joint:

    def __init__(self, position_m):
        self.position_m = position_m
        self.bodies = []

    def add_body(self, new_body):
        self.bodies.append(new_body)
        new_body.add_joint(self)


class BallJoint (Joint):

    def move(self, movement_m):
        for body in self.bodies:
            pass  # Todo: add functionality

    def update(self, stationary):
        position_on_body = sum([_ for joint, _ in stationary.joints
                                if joint is self], Vector((0, 0)))

        self.position_m = position_on_body + stationary.position_m
        for body in self.bodies:
            if body is not stationary:
                body.move_to_joint(self)


class BodyPart:

    proportions = {"Forearm": (10, 6.3), "Arm": (15, 5.2), "Neck": (15, 13),
                   "Head": 8, "Torso": (15, 2.2), "Thigh": (15, 4),
                   "Calf": (10, 4.2)}

#    def __init__(self, heigth_m, part, previous_joint):
#        self.upper_joint = previous
#        self.lower_joint = Joint(previous_joint + Vector(
#            0, heigth_m / BodyPart.proportions[part]))
#        self.length_m = FixedLengthConnection(
#            heigth_m / BodyPart.proportions, shoulder, self.elbow)


class Torso(BodyPart):

    def __init__(self, heigth_m):
        self.shape = Rectangle(BodyPart.proportions["Torso"][0], (
            heigth_m / BodyPart.proportions["Torso"][1]), Vector((0, 0)))


class Arm(BodyPart):

    def __init__(self, heigth_m):
        arm_heigth = heigth_m / BodyPart.proportions["Arm"][1]
        arm_position_y = (
            arm_heigth - heigth_m / BodyPart.proportions["Torso"][1]) / 2
        self.shape = Rectangle(BodyPart.proportions["Arm"][0], arm_heigth,
                               Vector((0, arm_position_y)))


class Forearm(BodyPart):

    def __init__(self, heigth_m):
        torso_heigth = heigth_m / BodyPart.proportions["Torso"][1]
        arm_heigth = heigth_m / BodyPart.proportions["Arm"][1]
        forearm_heigth = heigth_m / BodyPart.proportions["Forearm"][1]
        forearm_position_y = (forearm_heigth - torso_heigth) / 2 + arm_heigth
        self.shape = Rectangle(BodyPart.proportions["Forearm"][0],
                               forearm_heigth, Vector((0, forearm_position_y)))


class Thigh(BodyPart):

    def __init__(self, heigth_m):
        torso_heigth = heigth_m / BodyPart.proportions["Torso"][1]
        thigh_heigth = heigth_m / BodyPart.proportions["Thigh"][1]
        thigh_position_y = (torso_heigth + thigh_heigth) / 2
        self.shape = Rectangle(BodyPart.proportions["Thigh"][0], thigh_heigth,
                               Vector((0, thigh_position_y)))


class Neck(BodyPart):

    def __init__(self, heigth_m):
        torso_heigth = heigth_m / BodyPart.proportions["Torso"][1]
        neck_heigth = heigth_m / BodyPart.proportions["Neck"][1]
        neck_position_y = (neck_heigth - torso_heigth) / 2
        self.shape = Rectangle(BodyPart.proportions["Thigh"][0], neck_heigth,
                               Vector((0, neck_position_y)))


class Calf(BodyPart):

    def __init__(self, heigth_m):
        torso_heigth = heigth_m / BodyPart.proportions["Torso"][1]
        thigh_heigth = heigth_m / BodyPart.proportions["Thigh"][1]
        calf_heigth = heigth_m / BodyPart.proportions["Forearm"][1]
        calf_position_y = (calf_heigth + torso_heigth) / 2 + thigh_heigth
        self.shape = Rectangle(BodyPart.proportions["Forearm"][0], calf_heigth,
                               Vector((0, calf_position_y)))


class HumanRagdoll:

    def __init__(self, heigth_m, position_m=Vector(0, 0)):
        self.neck = Neck(heigth_m)
        self.torso = Torso(heigth_m)
        self.left_arm = Arm(heigth_m)
        self.right_arm = Arm(heigth_m)
        self.left_forearm = Forearm(heigth_m)
        self.right_forearm = Forearm(heigth_m)
        self.left_thigh = Thigh(heigth_m)
        self.right_thigh = Thigh(heigth_m)
        self.left_calf = Calf(heigth_m)
        self.right_calf = Calf(heigth_m)

        self.body_parts = [self.torso, self.neck, self.left_arm,
                           self.right_arm, self.left_forearm,
                           self.right_forearm, self.left_thigh,
                           self.right_thigh, self.left_calf, self.right_calf]

        for body_part in self.body_parts:
            events.right_button_selectable.append(body_part.shape)

        self.shoulders = BallJoint(Vector((0, self.torso.shape.heigth_m / -2)))
        self.hips = BallJoint(Vector((0, self.torso.shape.heigth_m / 2)))
        self.left_elbow = BallJoint(Vector((
            0, self.torso.shape.heigth_m / -2 + self.left_arm.shape.heigth_m)))
        self.right_elbow = BallJoint(Vector((
            0, self.torso.shape.heigth_m / -2 + self.right_arm.shape.heigth_m)))
        self.left_knee = BallJoint(Vector((
            0, self.torso.shape.heigth_m / 2 + self.left_thigh.shape.heigth_m)))
        self.right_knee = BallJoint(Vector((0, self.torso.shape.heigth_m / 2 +
                                            self.right_thigh.shape.heigth_m)))

        self.joints = [self.shoulders, self.hips, self.left_elbow,
                       self.right_elbow, self.left_knee, self.right_knee]

        self.shoulders.add_body(self.neck.shape)
        self.shoulders.add_body(self.torso.shape)
        self.shoulders.add_body(self.left_arm.shape)
        self.shoulders.add_body(self.right_arm.shape)
        self.hips.add_body(self.torso.shape)
        self.hips.add_body(self.left_thigh.shape)
        self.hips.add_body(self.right_thigh.shape)
        self.left_elbow.add_body(self.left_arm.shape)
        self.left_elbow.add_body(self.left_forearm.shape)
        self.right_elbow.add_body(self.right_arm.shape)
        self.right_elbow.add_body(self.right_forearm.shape)
        self.left_knee.add_body(self.left_thigh.shape)
        self.left_knee.add_body(self.left_calf.shape)
        self.right_knee.add_body(self.right_thigh.shape)
        self.right_knee.add_body(self.right_calf.shape)

        self.left_arm.shape.pull_on_anchor(Vector((0, 0)), position_m)

    def draw(self, surface):
        for body_part in self.body_parts:
            body_part.shape.draw(surface)

events = Events(2)
ragdoll = HumanRagdoll(170, Vector((250, 250)))

# rectangle = Rectangle(10, 50, Vector((250, 250)))
# rectangles = [Rectangle(10, 50, Vector((250, 200))),
#               Rectangle(10, 50, Vector((250, 300)))]
#
#
# joints = [BallJoint(Vector((250, 275))), BallJoint(Vector((250, 225)))]
#
# joints[0].add_body(rectangle)
# joints[0].add_body(rectangles[1])
# joints[1].add_body(rectangle)
# joints[1].add_body(rectangles[0])
#

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
        ragdoll.left_forearm.shape.move(Vector((-1, 0)))

    elif keys[pygame.K_RIGHT]:
        ragdoll.right_forearm.shape.move(Vector((1, 0)))

    elif keys[pygame.K_UP]:
        ragdoll.right_forearm.shape.rotate(1)

    elif keys[pygame.K_DOWN]:
        ragdoll.right_forearm.shape.rotate(-1)

    screen.fill((55, 155, 255))
    ragdoll.draw(screen)

#    else:
#        screen.fill((55, 155, 255))
#        rectangle.draw()

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
