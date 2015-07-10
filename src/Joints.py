from collections import OrderedDict

from pygame.math import Vector2 as Vector

from VectorMath import calculate_centroid, Line


class Joint:

    __counter = 0

    def __init__(self, bodies_positions):
        self._bodies_positions = bodies_positions
        for body in self._bodies_positions.keys():
            body.joints.append(self)
        # self.limited = False
        self.__hash_count = Joint.__counter
        Joint.__counter += 1

#    def add_body(self, new_body):
#        self.bodies.append(new_body)
#        new_body.add_joint(self)

    def __hash__(self):
        return self.__hash_count

    def __eq__(self, other):
        return all(key in other._bodies_positions.keys() and
                   self._bodies_positions[key] == other._bodies_positions[key]
                   for key in self._bodies_positions.keys()) and \
            isinstance(self, type(other))

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

    def calculate_world_position(self, base):
        return self.calculate_position(base) + base.position

    def calculate_position(self, base):
        return self._bodies_positions[base].rotate(round(
            Vector((1, 0)).angle_to(base.direction), 5))

    def calculate_pivot(self, body):
        connections = [joint._bodies_positions[body] for joint in body.joints
                       if joint != self]
        if not connections:
            return body.position
        return calculate_centroid(connections)


# class RailJoint(Joint):
#
#     def __init__(self, point_A, point_B):
#         Joint.__init__(self, {})
#         self.point_A = point_A
#         self.point_B = point_B
#
#     def __hash__(self):
#         return Joint.__hash__(self)
#
#     def __eq__(self, other):
#         return Joint.__eq__(self, other)
#
#     def move_to_joint(self, body):
#         anchor = self.calculate_world_position(body)
#         new_anchor = Line(
#             self.point_A, self.point_B, True).get_closest_point(
#             self.calculate_world_position(body))
#         magic = Vector(0, 0).rotate(
#             Vector((1, 0)).angle_to(body.direction)) + body.position
#         rotation = round((- magic).angle_to(new_anchor - magic), 5)
#         body.rotate(rotation)
#         anchor = (anchor - body.position).rotate(
#             rotation) + body.position
#         translation = new_anchor - anchor
#         body.move(translation)


class RevoluteJoint(Joint):

    def __init__(self, body_A, pos_on_body_A, body_B, pos_on_body_B):
        Joint.__init__(self, {body_A: pos_on_body_A,
                              body_B: pos_on_body_B})
        self.base = body_A
        self.mobile = body_B
        # self.__limit = (0, 90)
        # self.__motor = False
        self.apply_constraints(body_A)

#    def __hash__(self):
#        return Joint.__hash__(self)
#
#    def __eq__(self, other):
#        return Joint.__eq__(self, other)

#    @property
#    def limit(self):
#        return self.__limit

#    @property
#    def motor(self):
#        return self.__motor

#    @limit.setter
#    def limit(self, value):
#        self.__limit = (value + 360) % 360
#
#    @motor.setter
#    def motor(self, value):
#        pass

    def bent(self, angle):
        self.mobile.rotate_around(self._bodies_positions[self.mobile], angle)

    def set_bent(self, angle):
        """
        One should pass a value in the (0, 360) range to the angle argument!
        """
        self.bent(angle - self.calculate_angle_to_base())

    def bent_keeping_angles(self, angle):
        """
        This function preserves the angles between all RevoluteJoints related
        to the current.
        """
        joints_to_fix = OrderedDict()

        def find_messed(previous):
            for messed in previous.mobile.joints:
                if messed is not self and messed not in list(joints_to_fix.keys()) and \
                        messed is not previous and \
                        isinstance(messed, RevoluteJoint):
                    joints_to_fix[messed] = messed.calculate_angle_to_base()
                    find_messed(messed)
        for messed in self.mobile.joints:
            if messed is not self and messed not in list(joints_to_fix.keys()) and \
               isinstance(messed, RevoluteJoint):
                joints_to_fix[messed] = messed.calculate_angle_to_base()
                find_messed(messed)
        self.bent(angle)
        for joint in list(joints_to_fix.keys()):
            joint.set_bent(joints_to_fix[joint])
            joint.move_to_joint(joint.mobile)

    def calculate_angle_to_base(self):
        return self.calculate_position(
            self.base).angle_to(self.calculate_position(self.mobile)) % 360

    def other_body(self, current_body):
        return [_ for _ in self._bodies_positions.keys()
                if _ is not current_body][0]

    def move_to_joint(self, body):
        body.move(self.calculate_world_position(
            self.other_body(body)) - self.calculate_world_position(body))

    def pull_to_joint(self, body):
        joint_position = self.calculate_world_position(body)
        base = self.other_body(body)
        new_joint_position = self.calculate_world_position(base)
        magic = self.calculate_pivot(body).rotate(round(
            Vector((1, 0)).angle_to(body.direction), 5)) - body.position
        rotation = round((
            joint_position + magic).angle_to(new_joint_position + magic), 5)
        # work around a pygame bug
        rotation = (int(rotation * 100000) / 100000)
        joint_position = self.calculate_world_position(body)
        translation = new_joint_position - joint_position
        body.move(translation)
