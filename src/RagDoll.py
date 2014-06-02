import pygame

from pygame.math import Vector2 as Vector

from Joints import RevoluteJoint

from BasicShapes import Rectangle
from BasicShapes import Circle
from BasicShapes import Triangle


class BodyPart:
    proportions = {"Forearm": (10, 4.3), "Arm": (15, 3.2), "Neck": (15, 13),
                   "Head": (5, 5), "Torso": (20, 2.2), "Thigh": (15, 3.2),
                   "Calf": (10, 4.3)}

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__repr__()


class Head(BodyPart, Circle):

    def __init__(self, height_m):
        torso_height = height_m / BodyPart.proportions["Torso"][1] / 2
        neck_height = height_m / BodyPart.proportions["Neck"][1]
        head_radius = height_m / BodyPart.proportions["Head"][0] / 2
        head_position_y = - neck_height - head_radius - torso_height
        Circle.__init__(self, head_radius, Vector((0, head_position_y)))


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
        Rectangle.__init__(self, BodyPart.proportions["Neck"][0], neck_height,
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
        self.height_m = height_m

        # creating body_parts
        self.head = Head(height_m)
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

        # creating pivots for better rotation
        self.head.pivot_m = Vector((0, self.head.radius_m))
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

        # creating joints
        self.atlas = RevoluteJoint(
            self.head, Vector((0, self.head.radius_m)),
            self.neck, Vector((0, self.neck.height_m / -2)))
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

        self.body_parts = [self.torso, self.neck, self.left_arm,
                           self.right_arm, self.left_forearm,
                           self.right_forearm, self.left_thigh,
                           self.right_thigh, self.left_calf,
                           self.right_calf, self.head]

    def load_avatars(self, folder):
        try:
            for body_part in self.body_parts:
                body_part.imageMaster = pygame.image.load(
                    r"../ArtWork/Ragdolls/{0}/{1}.png".format(
                        folder, body_part)).convert_alpha()
                body_part.scale_avatar(
                    body_part.imageMaster.get_width() / 2.5,
                    body_part.imageMaster.get_height() / 2.5)
        except pygame.error:
            self.display_avatar = self.draw

    def draw(self, surface):
        for body_part in self.body_parts:
            body_part.draw(surface)

    def display_avatar(self, surface):
        for body_part in self.body_parts:
            body_part.display_avatar(surface)
