import math
import sys
import pygame

from VectorMath import seperate_point
from Events import Events
from Control import Control

from pygame.math import Vector2 as Vector

from collections import OrderedDict
from _collections import defaultdict

from BasicShapes import Rectangle

pygame.init()

screen = pygame.display.set_mode((500, 500))

clock = pygame.time.Clock()


class Joint:

    def __init__(self, bodies_positions):
        self._bodies_positions = bodies_positions
        for body in self._bodies_positions.keys():
            body.joints.append(self)

#    def add_body(self, new_body):
#        self.bodies.append(new_body)
#        new_body.add_joint(self)

    def calculate_position_m(self, body):
        return self._bodies_positions[body].rotate(
            Vector((1, 0)).angle_to(body.direction)) + body.position_m


class RevoluteJoint(Joint):  # might neet to create another type of joint

    def __init__(self, body_A, pos_on_body_A_m, body_B, pos_on_body_B_m):
        Joint.__init__(self, {body_A: pos_on_body_A_m,
                              body_B: pos_on_body_B_m})
        self.apply_constraints(body_A)

    def other_body(self, current_body):
        return [_ for _ in self._bodies_positions.keys()
                if _ is not current_body][0]

    def apply_constraints(self, stationary):
        stationary_bodies = set([stationary])

        def recursive_fix(self, stationary):
            not_stationary = self.other_body(stationary)
            self.move_to_joint(not_stationary)
            stationary_bodies.add(not_stationary)
            for joint in not_stationary.joints:
                if joint is not self and isinstance(joint, type(self)) and \
                   joint.other_body(not_stationary) not in stationary_bodies:
                    recursive_fix(joint, not_stationary)
        recursive_fix(self, stationary)

    def move_to_joint(self, body):
        joint_position = self.calculate_position_m(body)
        base = self.other_body(body)
        new_joint_position = self.calculate_position_m(base)
        magic = body.pivot_m.rotate(
            Vector((1, 0)).angle_to(body.direction)) - body.position_m
        rotation = (
            joint_position + magic).angle_to(new_joint_position + magic)
        # work around a pygame bug
        rotation = int(rotation * 100000) / 100000
        if abs(body.pivot_m.x - self._bodies_positions[body].x) < 0.01 and \
                abs(body.pivot_m.y - self._bodies_positions[body].y) < 0.01:
            body.rotate(rotation)
        joint_position = self.calculate_position_m(body)
        translation = new_joint_position - joint_position
        body.move(translation)


class BodyPart:
    proportions = {"Forearm": (10, 4.3), "Arm": (15, 3.2), "Neck": (15, 13),
                   "Head": 8, "Torso": (20, 2.2), "Thigh": (15, 3.2),
                   "Calf": (10, 4.3)}

#    def __init__(self, height_m, part, previous_joint):
#        self.upper_joint = previous
#        self.lower_joint = Joint(previous_joint + Vector(
#            0, height_m / BodyPart.proportions[part]))
#        self.length_m = FixedLengthConnection(
#                 height_m / BodyPart.proportions,
#                 shoulder, self.elbow)


class Torso(BodyPart, Rectangle):

    def __init__(self, height_m):
        Rectangle.__init__(self, BodyPart.proportions["Torso"][0], (height_m /
                           BodyPart.proportions["Torso"][1]), Vector((0, 0)))


class Arm(BodyPart, Rectangle):

    def __init__(self, height_m):
        arm_height = height_m / BodyPart.proportions["Arm"][1]
        arm_position_y = (
            arm_height - height_m / BodyPart.proportions["Torso"][1]) / 2
        Rectangle.__init__(self, BodyPart.proportions["Arm"][0], arm_height,
                           Vector((0, arm_position_y)))


class Forearm(BodyPart, Rectangle):

    def __init__(self, height_m):
        torso_height = height_m / BodyPart.proportions["Torso"][1]
        arm_height = height_m / BodyPart.proportions["Arm"][1]
        forearm_height = height_m / BodyPart.proportions["Forearm"][1]
        forearm_position_y = (forearm_height - torso_height) / 2 + arm_height
        Rectangle.__init__(self, BodyPart.proportions["Forearm"][0],
                           forearm_height, Vector((0, forearm_position_y)))


class Thigh(BodyPart, Rectangle):

    def __init__(self, height_m):
        torso_height = height_m / BodyPart.proportions["Torso"][1]
        thigh_height = height_m / BodyPart.proportions["Thigh"][1]
        thigh_position_y = (torso_height + thigh_height) / 2
        Rectangle.__init__(
            self, BodyPart.proportions["Thigh"][0], thigh_height,
            Vector((0, thigh_position_y)))


class Neck(BodyPart, Rectangle):

    def __init__(self, height_m):
        torso_height = height_m / BodyPart.proportions["Torso"][1]
        neck_height = height_m / BodyPart.proportions["Neck"][1]
        neck_position_y = (neck_height - torso_height) / 2
        Rectangle.__init__(self, BodyPart.proportions["Thigh"][0], neck_height,
                           Vector((0, neck_position_y)))


class Calf(BodyPart, Rectangle):

    def __init__(self, height_m):
        torso_height = height_m / BodyPart.proportions["Torso"][1]
        thigh_height = height_m / BodyPart.proportions["Thigh"][1]
        calf_height = height_m / BodyPart.proportions["Calf"][1]
        calf_position_y = (calf_height + torso_height) / 2 + thigh_height
        Rectangle.__init__(self, BodyPart.proportions["Calf"][0], calf_height,
                           Vector((0, calf_position_y)))


class HumanRagdoll:

    def __init__(self, height_m, position_m=Vector(0, 0)):
        self.neck = Neck(height_m)
        self.torso = Torso(height_m)
        self.left_arm = Arm(height_m)
        self.right_arm = Arm(height_m)
        self.left_forearm = Forearm(height_m)
        self.right_forearm = Forearm(height_m)
        self.left_thigh = Thigh(height_m)
        self.right_thigh = Thigh(height_m)
        self.left_calf = Calf(height_m)
        self.right_calf = Calf(height_m)

        self.neck.pivot_m = Vector((0, self.neck.height_m / 2))
        self.torso.pivot_m = Vector((0, self.torso.height_m / 2))
        self.left_arm.pivot_m = Vector((0, self.left_arm.height_m / -2))
        self.right_arm.pivot_m = Vector((0, self.right_arm.height_m / -2))
        self.left_forearm.pivot_m = Vector(
            (0, self.left_forearm.height_m / -2))
        self.right_forearm.pivot_m = Vector(
            (0, self.right_forearm.height_m / -2))
        self.left_thigh.pivot_m = Vector((0, self.left_thigh.height_m / -2))
        self.right_thigh.pivot_m = Vector((0, self.right_thigh.height_m / -2))
        self.left_calf.pivot_m = Vector((0, self.left_calf.height_m / -2))
        self.right_calf.pivot_m = Vector((0, self.right_calf.height_m / -2))

     #   self.neck.shape.imageMaster = pygame.image.load(
     #       r"../ArtWork/Ragdolls/Batman/Neck.png").convert_alpha()
     #   self.torso.shape.imageMaster = pygame.image.load(
     #       r"../ArtWork/Ragdolls/Batman/Torso.png").convert_alpha()
     #   self.left_arm.shape.imageMaster = pygame.image.load(
     #       r"../ArtWork/Ragdolls/Batman/Arm.png").convert_alpha()
     #   self.right_arm.shape.imageMaster = pygame.image.load(
     #       r"../ArtWork/Ragdolls/Batman/Arm.png").convert_alpha()
     #   self.left_forearm.shape.imageMaster = pygame.image.load(
     #       r"../ArtWork/Ragdolls/Batman/Forearm.png").convert_alpha()
     #   self.right_forearm.shape.imageMaster = pygame.image.load(
     #       r"../ArtWork/Ragdolls/Batman/Forearm.png").convert_alpha()
     #   self.left_thigh.shape.imageMaster = pygame.image.load(
     #       r"../ArtWork/Ragdolls/Batman/Thigh.png").convert_alpha()
     #   self.right_thigh.shape.imageMaster = pygame.image.load(
     #       r"../ArtWork/Ragdolls/Batman/Thigh.png").convert_alpha()
     #   self.left_calf.shape.imageMaster = pygame.image.load(
     #       r"../ArtWork/Ragdolls/Batman/Calf.png").convert_alpha()
     #   self.right_calf.shape.imageMaster = pygame.image.load(
     #       r"../ArtWork/Ragdolls/Batman/Calf.png").convert_alpha()

        self.body_parts = [self.torso, self.neck, self.left_arm,
                           self.right_arm, self.left_forearm,
                           self.right_forearm, self.left_thigh,
                           self.right_thigh, self.left_calf, self.right_calf]

        for body_part in self.body_parts:
            control.left_button_selectable.append(body_part)
        #    body_part.shape.scale_avatar()

        self.collar = RevoluteJoint(
            self.neck, Vector((0, self.neck.height_m / 2)),
            self.torso, Vector((0, self.torso.height_m / -2)))
        self.left_shoulder = RevoluteJoint(
            self.torso, Vector((0, self.torso.height_m / -2)),
            self.left_arm, Vector((0, self.left_arm.height_m / -2)))
        self.right_shoulder = RevoluteJoint(
            self.torso, Vector((0, self.torso.height_m / -2)),
            self.right_arm, Vector((0, self.right_arm.height_m / -2)))
        self.left_hip = RevoluteJoint(
            self.torso, Vector((0, self.torso.height_m / 2)),
            self.left_thigh, Vector((0, self.left_thigh.height_m / -2)))
        self.right_hip = RevoluteJoint(
            self.torso, Vector((0, self.torso.height_m / 2)),
            self.right_thigh, Vector((0, self.right_thigh.height_m / -2)))
        self.left_elbow = RevoluteJoint(
            self.left_arm, Vector((0, self.left_arm.height_m / 2)),
            self.left_forearm, Vector((0, self.left_forearm.height_m / -2)))
        self.right_elbow = RevoluteJoint(
            self.right_arm, Vector((0, self.right_arm.height_m / 2)),
            self.right_forearm, Vector((0, self.right_forearm.height_m / -2)))
        self.left_knee = RevoluteJoint(
            self.left_thigh, Vector((0, self.left_thigh.height_m / 2)),
            self.left_calf, Vector((0, self.left_calf.height_m / -2)))
        self.right_knee = RevoluteJoint(
            self.right_thigh, Vector((0, self.left_thigh.height_m / 2)),
            self.right_calf, Vector((0, self.right_calf.height_m / -2)))

       # self.joints = [self.shoulders, self.hips, self.left_elbow,
       # self.right_elbow, self.left_knee, self.right_knee]

        self.left_arm.pull_on_anchor(Vector((0, 0)), position_m)

    def draw(self, surface):
        for body_part in self.body_parts:
            body_part.draw(surface)

    def display_avatar(self, surface):
        for body_part in self.body_parts:
            body_part.display_avatar(surface)

control = Control(2)
ragdoll = HumanRagdoll(170, Vector((250, 250)))
counter = 0

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
        ragdoll.left_forearm.move(Vector((-1, 0)))

    elif keys[pygame.K_RIGHT]:
        ragdoll.right_forearm.move(Vector((1, 0)))

    elif keys[pygame.K_UP]:
        ragdoll.right_forearm.rotate(1)

    elif keys[pygame.K_DOWN]:
        ragdoll.right_forearm.rotate(-1)

    screen.fill((55, 155, 255))
    ragdoll.draw(screen)
   # ragdoll.display_avatar(screen)

#    else:
#        screen.fill((55, 155, 255))
#        rectangle.draw()

    # pygame.draw.polygon(screen, (255, 255, 255),
    #                    [(0, 0), (0, 50), (50, 50), (50, 0)])
    pygame.display.update()
    clock.tick(60)

    control.handle_user_input()

# class BodyPart:
#
#     proportions = {"Forearm": 6.3, "Arm": 5.2, "Neck": 13, "Head": 8,
#                    "Torso": 2.2, "Thigh": 4, "Calf": 4.2}
#
#     def __init__(self, height_m, part, previous_joint):
#         self.upper_joint = previous
#         self.lower_joint = Joint(previous_joint + Vector(
#             0, height_m / BodyPart.proportions[part]))
#         self.length_m = FixedLengthConnection(
#             height_m / BodyPart.proportions, shoulder, self.elbow)
#
#
# class HumanRagdoll(FixedLengthJointSystem):
#
#     def __init__(self, height_m, position_m=Vector(0, 0)):
#         self.joints = {"Head": Joint(position_m)}
#         self.body_parts = {
#             "Head": BodyPart(height_m, "Head", self.joints["Head"])}
#         self.joints.append(self.body_parts["Head"].lower_joint)
#         self.body_parts["Neck"] = BodyPart(height_m, "Neck"
