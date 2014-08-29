import pygame
from collections import OrderedDict
from pickle import load


from pygame.math import Vector2 as Vector

from Joints import RevoluteJoint

from BasicShapes import SHAPES
from VectorMath import Line


class HumanRagdoll:

    def __init__(self, name="default"):
        self.load_dimensions(name)
        self.body_parts = OrderedDict([
            (body_part, self.create_body_part(body_part))
            for body_part in self.body_part_dimensions])
        self.joints = {joint: self.create_joint(joint)
                       for joint in self.joint_placement}
        self.load_avatars(name)
        self.body_parts["torso"].pivot_m = Vector(
            (0, self.body_parts["torso"].height_m / 2))
        self.__facing = "right"

    @property
    def facing(self):
        return self.__facing

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

    @property
    def direction(self):
        return self.body_parts["torso"].direction

    def turn(self, direction):
        if self.facing == direction or direction not in ["right", "left"]:
            return
        else:
            perpendicular = Vector(1, 0).rotate(90)
            for body_part in self.body_parts.values():
                body_part.reflect(
                    Line(self.position, self.position + perpendicular))
            self.__facing = direction

    def calculate_slope(self):
        return self.direction.angle_to(Vector(1, 0)) % 360

    def set_slope(self, angle):
        self.rotate(self.calculate_slope() - angle)

    def create_body_part(self, body_part):
        if self.body_part_dimensions[body_part][0] == "Triangle":
            return SHAPES["Triangle"]([Vector(
                *[dimension[_] / self.proportions[0] for _ in range(2)])
                for dimension in self.body_part_dimensions[body_part][1]])
        else:
            return SHAPES[self.body_part_dimensions[body_part][0]](
                *[dimension / self.proportions[0]
                  for dimension in self.body_part_dimensions[body_part][1:]])

    def create_joint(self, joint):
        self.body_parts[self.joint_placement[joint][2]].pivot_m = Vector(
            self.joint_placement[joint][3]) / self.proportions[1]
        return RevoluteJoint(
            self.body_parts[self.joint_placement[joint][0]],
            Vector(self.joint_placement[joint][1]) / self.proportions[1],
            self.body_parts[self.joint_placement[joint][2]],
            Vector(self.joint_placement[joint][3]) / self.proportions[1])

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

    def capture_frame(self):
        if self.facing == "left":
            frame = {joint: 360 - self.joints[joint].calculate_angle_to_base()
                     for joint in self.joints.keys()}
            frame["slope"] = 360 - self.calculate_slope()
            return frame
        frame = {joint: self.joints[joint].calculate_angle_to_base()
                 for joint in self.joints.keys()}
        frame["slope"] = self.calculate_slope()
        return frame

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

    def shift_to_next_frame(self, previous_frame, next_frame):
        difference = {key:  next_frame[key] - previous_frame[key]
                      for key in next_frame}
        if difference["slope"] > 180:
            difference["slope"] = difference["slope"] - 360
        if difference["slope"] < -180:
            difference["slope"] = difference["slope"] + 360
        if self.facing == "left":
            difference["slope"] *= -1
        for frame in range(25):
            for joint in self.joints:
                angle = difference[joint]
                if angle > 180:
                    angle = angle - 360
                if angle < -180:
                    angle = angle + 360
                if self.facing == "left":
                    angle *= -1
                self.joints[joint].bent_keeping_angles(angle / 25)
            self.rotate(difference["slope"] / 25)
            yield
        raise StopIteration

    def rotate(self, angle):
        for part in self.body_parts.values():
            part.rotate_around(part.position_on_body(self.position), angle)

    def move(self, movement):
        for part in self.body_parts.values():
            part.move(movement)

    def load_avatars(self, folder):
        try:
            for body_part in self.body_parts:
                self.body_parts[body_part].load_avatar(r"{0}/{1}.png".format(
                    folder, body_part))
                self.body_parts[body_part].scale_avatar(
                    self.body_parts[body_part].imageMaster.get_width()
                    / self.proportions[1],
                    self.body_parts[body_part].imageMaster.get_height()
                    / self.proportions[1])
        except pygame.error:
            self.display_avatar = self.draw

    def draw(self, surface):
        for body_part in self.body_parts.values():
            body_part.draw(surface)

    def display_avatar(self, surface):
        for body_part in self.body_parts.values():
            body_part.display_avatar(surface)

    def orientate_feet(self, floor):
        pass
