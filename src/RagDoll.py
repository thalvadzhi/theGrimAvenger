import pygame
from collections import OrderedDict
from pickle import load


from pygame.math import Vector2 as Vector

from Joints import RevoluteJoint

from BasicShapes import SHAPES


# class BodyPart:
#     __proportions = OrderedDict([("left_forearm", ("Rectangle", 85, 180)),
#                                  ("left_arm", ("Rectangle", 80, 150)),
#                                  ("left_boot",
#                                   ("Triangle", ((0, 0), (123/5, 0), (26/5, -68/5)))),
#                                  ("left_calf", ("Rectangle", 83, 218)),
#                                  ("left_thigh", ("Rectangle", 97, 225)),
#                                  ("neck", ("Rectangle", 72, 128)),
#                                  ("torso", ("Rectangle", 123, 262)),
#                                  ("head", ("Circle", 61)),
#                                  ("right_thigh", ("Rectangle", 97, 225)),
#                                  ("right_calf", ("Rectangle", 83, 218)),
#                                  ("right_boot",
#                                   ("Triangle", ((0, 0), (123/5, 0), (26/5, -68/5)))),
#                                  ("right_arm", ("Rectangle", 80, 150)),
#                                  ("right_forearm", ("Rectangle", 85, 180))])
#
#     @classmethod
#     def proportions(cls):
#         return cls.__proportions
#
#     def __repr__(self):
#         return self.body_part
#
#     def __str__(self):
#         return self.body_part

      #     {"atlas": ("neck", (0, -30), "head", (-20, 40)),
      #      "collar": ("torso", (-26, -97), "neck", (-1.5, 29.5)),
      #      "left_shoulder": ("torso", (-26, -97), "left_arm", (3, -40)),
      #      "right_shoulder": ("torso", (-26, -97), "right_arm", (3, -40)),
      #      "left_hip": ("torso", (-1, 87.5), "left_thigh", (-6, -70)),
      #      "right_hip": ("torso", (-1, 87.5), "right_thigh", (-6, -70)),
      #      "left_elbow": ("left_arm", (-7.5, 49), "left_forearm", (14, -64.5)),
      #      "right_elbow": ("right_arm", (-7.5, 49), "right_forearm", (14, -64.5)),
      #      "left_knee": ("left_thigh", (7.5, 85.5), "left_calf", (12.5, -82.5)),
      #      "right_knee": ("right_thigh", (7.5, 85.5), "right_calf", (12.5, -82.5)),
      #      "left_ankle": ("left_calf", (-2.5, 82), "left_boot", (-30.5, -8)),
      #      "right_ankle": ("right_calf", (-2.5, 82), "right_boot", (-30.5, -8))}


class HumanRagdoll:

    def __init__(self, name="default"):
        self.load_dimensions(name)
        self.body_parts = OrderedDict([
            (body_part, self.create_body_part(body_part))
            for body_part in self.body_part_dimensions])
        self.joints = {joint: self.create_joint(joint)
                       for joint in self.joint_placement}
        self.load_avatars(name)
      #  for part in self.body_parts:
      #      setattr(self, part, self.body_parts[part])

  # creating pivots for better rotation
  # the pivots will be removed
  #      self.head.pivot_m = Vector((0, self.head.radius_m))
  #      self.neck.pivot_m = Vector((0, self.neck.height_m / 2))
        self.body_parts["torso"].pivot_m = Vector(
            (0, self.body_parts["torso"].height_m / 2))
  #      self.left_arm.pivot_m = Vector((0, self.left_arm.height_m / -2))
  #      self.right_arm.pivot_m = Vector((0, self.right_arm.height_m / -2))
  #      self.left_forearm.pivot_m = Vector(
  #          (0, self.left_forearm.height_m / -2))
  #      self.right_forearm.pivot_m = Vector(
  #          (0, self.right_forearm.height_m / -2))
  #      self.left_thigh.pivot_m = Vector((0, self.left_thigh.height_m / -2))
  #      self.right_thigh.pivot_m = Vector((0, self.right_thigh.height_m / -2))
  #      self.left_calf.pivot_m = Vector((0, self.left_calf.height_m / -2))
  #      self.right_calf.pivot_m = Vector((0, self.right_calf.height_m / -2))
  #      self.left_boot.pivot_m = Vector((-30.5, -8)) / 5
  #      self.right_boot.pivot_m = Vector((-30.5, -8)) / 5

  # creating joints
  #      self.atlas = RevoluteJoint(
  #          self.neck, Vector((0, -30))/5, self.head, Vector((-20, 40))/5)
  #      self.collar = RevoluteJoint(
  #          self.torso, Vector((-26, -97))/5, self.neck, Vector((-1.5, 29.5))/5)
  #      self.left_shoulder = RevoluteJoint(
  #          self.torso, Vector((-26, -97))/5, self.left_arm, Vector((3, -40))/5)
  #      self.right_shoulder = RevoluteJoint(
  #          self.torso, Vector((-26, -97))/5, self.right_arm, Vector((3, -40))/5)
  #      self.left_hip = RevoluteJoint(
  #          self.torso, Vector((-1, 87.5))/5,
  #          self.left_thigh, Vector((-6, -70))/5)
  #      self.right_hip = RevoluteJoint(
  #          self.torso, Vector((-1, 87.5))/5,
  #          self.right_thigh, Vector((-6, -70))/5)
  #      self.left_elbow = RevoluteJoint(
  #          self.left_arm, Vector((-7.5, 49))/5,
  #          self.left_forearm, Vector((14, -64.5))/5)
  #      self.right_elbow = RevoluteJoint(
  #          self.right_arm, Vector((-7.5, 49))/5,
  #          self.right_forearm, Vector((14, -64.5))/5)
  #      self.left_knee = RevoluteJoint(
  #          self.left_thigh, Vector((7.5, 85.5))/5,
  #          self.left_calf, Vector((12.5, -82.5))/5)
  #      self.right_knee = RevoluteJoint(
  #          self.right_thigh, Vector((7.5, 85.5))/5,
  #          self.right_calf, Vector((12.5, -82.5))/5)
  #      self.left_ankle = RevoluteJoint(
  #          self.left_calf, Vector((-2.5, 82))/5,
  #          self.left_boot, Vector((-30.5, -8))/5)
  #      self.right_ankle = RevoluteJoint(
  #          self.right_calf, Vector((-2.5, 82))/5,
  #          self.right_boot, Vector((-30.5, -8))/5)

  #      self.joints = {"atlas": self.atlas,
  #                     "collar": self.collar,
  #                     "left_shoulder": self.left_shoulder,
  #                     "right_shoulder": self.right_shoulder,
  #                     "left_hip": self.left_hip,
  #                     "right_hip": self.right_hip,
  #                     "left_elbow": self.left_elbow,
  #                     "right_elbow": self.right_elbow,
  #                     "left_knee": self.left_knee,
  #                     "right_knee": self.right_knee,
  #                     "left_ankle": self.left_ankle,
  #                     "right_ankle": self.right_ankle}

    @property
    def proportions(self):
        return self.__proportions

    @property
    def joint_placement(self):
        return self.__joint_placement

    @property
    def body_part_dimensions(self):
        return self.__body_part_dimensions

    @property
    def position(self):
        return self.body_parts["torso"].position_m

    def create_body_part(self, body_part):
        return SHAPES[self.body_part_dimensions[body_part][0]](
            *[dimension / self.proportions[0]
              for dimension in self.body_part_dimensions[body_part][1:]])

    def create_joint(self, joint):
        self.body_parts[self.joint_placement[joint][2]].pivot_m = Vector(
            self.joint_placement[joint][3]) / self.proportions[0]
        return RevoluteJoint(
            self.body_parts[self.joint_placement[joint][0]],
            Vector(self.joint_placement[joint][1]) / self.proportions[0],
            self.body_parts[self.joint_placement[joint][2]],
            Vector(self.joint_placement[joint][3]) / self.proportions[0])

    def load_dimensions(self, name="default"):
        try:
            with open(
                    r"../ArtWork/Ragdolls/{0}/body_part_dimensions".format(name),
                    "rb") as dimensions:
                self.__proportions = load(dimensions)
                self.__body_part_dimensions = OrderedDict(load(dimensions))
            with open(r"../ArtWork/Ragdolls/{0}/joint_placement".format(name),
                      "rb") as placement:
                self.__joint_placement = load(placement)
        except IOError:
            self.load_dimensions()

    def calculate_state(self):
        return {joint: self.joints[joint].calculate_angle_to_base()
                for joint in self.joints.keys()}

    def save_state(self):
        return {body_part: (self.body_parts[body_part].direction,
                            self.body_parts[body_part].position_m -
                            self.position)
                for body_part in self.body_parts}

    def set_state(self, state):
        current_position = self.position
        for body_part in self.body_parts:
            self.body_parts[body_part].direction = state[body_part][0]
            self.body_parts[body_part].position_m = \
                state[body_part][1] + current_position
        self.body_parts["torso"].fix_joints()

    def shift_to_next_state(self, difference, frames):
        for joint in self.joints:
            angle = difference[joint]
            if angle > 180:
                angle = angle - 360
            if angle < -180:
                angle = angle + 360
            self.joints[joint].bent_keeping_angles(angle / frames)

    def rotate(self, angle):
        for part in self.body_parts.values():
            part.rotate_around(self.position, angle)

    def move(self, movement):
        for part in self.body_parts.values():
            part.move(movement)

    def load_avatars(self, folder):
        try:
            for body_part in self.body_parts.values():
                body_part.imageMaster = pygame.image.load(
                    r"../ArtWork/Ragdolls/{0}/{1}.png".format(
                        folder, body_part)).convert_alpha()
                body_part.scale_avatar(
                    body_part.imageMaster.get_width() / self.proportions[1],
                    body_part.imageMaster.get_height() / self.proportions[1])
        except pygame.error:
            self.display_avatar = self.draw

    def draw(self, surface):
        for body_part in self.body_parts.values():
            body_part.draw(surface)

    def display_avatar(self, surface):
        for body_part in self.body_parts.values():
            body_part.display_avatar(surface)
