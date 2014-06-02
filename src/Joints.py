from pygame.math import Vector2 as Vector


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
        self.__limit = 180
        self.__motor = False
        self.apply_constraints(body_A)

    @property
    def limit(self):
        return self.__limit

    @property
    def motor(self):
        return self.__motor

    @limit.setter
    def limit(self, value):
        self.__limit = (value + 360) % 360

    @motor.setter
    def motor(self, value):
        pass

    def calc_angle_to_base(self, body):
        return body.direction.angle_to(self.other_body(body).direction)

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
        rotation = (int(rotation * 100000) / 100000)
     #   angle_between_bodies = self.calc_angle_to_base(body)
     #   if (angle_between_bodies + 360) % 360 > self.limit:
     #       body.rotate(- angle_between_bodies - self.limit)
        if abs(body.pivot_m.x - self._bodies_positions[body].x) < 0.01 and \
                abs(body.pivot_m.y - self._bodies_positions[body].y) < 0.01:
            body.rotate(rotation)
        joint_position = self.calculate_position_m(body)
        translation = new_joint_position - joint_position
        body.move(translation)
