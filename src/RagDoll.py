from collections import OrderedDict
from math import copysign
from pickle import load

import pygame
from pygame.math import Vector2 as Vector

import Physics
from Joints import RevoluteJoint
from Motions import Motion
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
        self.body_parts["torso"].pivot = Vector(
            (0, self.body_parts["torso"].height / 2))
        self.__facing = "right"
        self.velocity = Vector(0.0, 0.0)
        self.impulse = Vector(0.0, 0.0)
        self.__mass = sum([body_part.mass
                           for body_part in self.body_parts.values()])
        self.motion = Motion(self)

    @property
    def mass(self):
        return self.__mass

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
        return self.body_parts["torso"].position

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
        self.body_parts[self.joint_placement[joint][2]].pivot = Vector(
            self.joint_placement[joint][3]) / self.proportions[1]
        return RevoluteJoint(
            self.body_parts[self.joint_placement[joint][0]],
            Vector(self.joint_placement[joint][1]) / self.proportions[1],
            self.body_parts[self.joint_placement[joint][2]],
            Vector(self.joint_placement[joint][3]) / self.proportions[1])

    def load_dimensions(self, name="default"):
        try:
            with open(r"../ArtWork/Ragdolls/{0}/body_part_dimensions".format(
                    name), "rb") as dimensions:
                self.__proportions = load(dimensions)
                self.__body_part_dimensions = OrderedDict(load(dimensions))
            with open(r"../ArtWork/Ragdolls/{0}/joint_placement".format(name),
                      "rb") as placement:
                self.__joint_placement = load(placement)
        except IOError:
            self.load_dimensions()

    def hand_position(self, leftedness):
        forearm = self.body_parts["{0}_forearm".format(leftedness)]
        return (forearm.vertices[0] + forearm.vertices[1]) / 2 
        # bone = (forearm.vertices[0] +
        #        forearm.vertices[1]) / 2 - forearm.position
        # return forearm.position + bone + bone.normalize() * 5

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
                            self.body_parts[body_part].position -
                            self.position)
                for body_part in self.body_parts}

    def set_state(self, state):
        current_position = self.position
        for body_part in self.body_parts:
            self.body_parts[body_part].direction = state[body_part][0]
            self.body_parts[body_part].position = \
                state[body_part][1] + current_position
        self.body_parts["torso"].fix_joints()

    def calculate_frame_difference(self, frame):
        previous_frame = self.capture_frame()
        frame = {key: frame[key] - previous_frame[key]
                      for key in previous_frame}
        for joint in self.joints:
            if frame[joint] > 180 or frame[joint] < -180:
                frame[joint] -= copysign(360, frame[joint])
        if frame["slope"] > 180 or frame["slope"] < -180:
            frame["slope"] -= copysign(360, frame["slope"])
        return frame

    def set_frame(self, frame):
        frame = self.calculate_frame_difference(frame)
        facing = {"left": -1, "right": 1}[self.facing]
        for joint in self.joints:
            self.joints[joint].bent_keeping_angles(frame[joint] * facing)
        self.rotate(frame["slope"] * -facing)

    def shift_to_frame(self, frame, start_time, clock):
        duration = frame["duration"]
        frame = self.calculate_frame_difference(frame)
        elapsed_time = 0
        bent_fraction = 0
        while elapsed_time < duration:
            facing = {"left": -1, "right": 1}[self.facing]
            elapsed_time = clock.get_ticks() - start_time
            fraction = elapsed_time / duration - bent_fraction
            if elapsed_time > duration:
                fraction = 1 - bent_fraction
            bent_fraction += fraction
            for joint in self.joints:
                self.joints[joint].bent_keeping_angles(frame[joint] * fraction * facing)
            self.rotate(frame["slope"] * fraction * -facing)
            yield
        raise StopIteration

    def rotate(self, angle):
        for part in self.body_parts.values():
            part.rotate_around(part.position_on_body(self.position), angle)

    def move(self, movement):
        for part in self.body_parts.values():
            part.move(movement)

    def load_avatars(self, folder):
        for body_part in self.body_parts:
            self.body_parts[body_part].load_avatar(
                r"Ragdolls/{0}/{1}.png".format(folder, body_part))
            self.body_parts[body_part].scale_avatar(
                self.body_parts[body_part].image_master.get_width()
                / self.proportions[1],
                self.body_parts[body_part].image_master.get_height()
                / self.proportions[1])

    def apply_physics(self, time):
        Physics.apply_gravity(self, time)
        self.move(self.velocity)

    def draw(self, surface, camera=0):
        for body_part in self.body_parts.values():
            body_part.draw(surface, camera)

    def display_avatar(self, surface, camera=0):
        for body_part in self.body_parts.values():
            body_part.display_avatar(surface, camera)

    def orientate_feet(self, floor):
        pass


# class NPC(HumanRagdoll):
#
#     observance_levels = {
#         "easy": (10, 20),
#         "normal": (20, 30),
#         "hard": (30, 40),
#         "insane": (40, 50)
#     }
#
#     def __init__(self, observance, NPC_type="trooper"):
#         HumanRagdoll.__init__(self, "NPC_{0}".format(NPC_type))
#         self.NPC_type = NPC_type
#         self.observance = observance
#         self.alerted = False
#
#     def check_if_hears(self, sounds):
#         for sound in sounds:
#             if SHAPES["Circle"](NPC.observance_levels[self.observance][0],
#                                 sound).check_if_collide(
#                     self.body_parts["head"])[0]:
#                 self.alerted = True
