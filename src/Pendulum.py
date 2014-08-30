from math import sin, cos, radians
from BasicShapes import Rectangle


class Pendulum:
    def __init__(self, angle, swing_length, pivot):
        self.theta = angle
        self.dtheta = 0
        self.swing_length = swing_length
        self.pivot = pivot
        self.time = 0
        self.rect = Rectangle(1, 1,
                              (int(self.pivot[0] - self.swing_length * cos(radians(self.theta))),
                              int(self.pivot[1] + self.swing_length * sin(radians(self.theta)))))

    def recompute_angle(self):
        self.time += 1
        #modulates gravity
        scaling = 2000 / (self.swing_length ** 2)

        first_d_d_theta = -sin(radians(self.theta)) * scaling
        mid_d_theta = self.dtheta + first_d_d_theta
        midtheta = self.theta + (self.dtheta + mid_d_theta) / 2.0

        mid_d_d_theta = -sin(radians(midtheta)) * scaling
        mid_d_theta = self.dtheta + (first_d_d_theta + mid_d_d_theta) / 2
        midtheta = self.theta + (self.dtheta + mid_d_theta) / 2

        mid_d_d_theta = -sin(radians(midtheta)) * scaling
        last_d_theta = mid_d_theta + mid_d_d_theta
        lasttheta = midtheta + (mid_d_theta + last_d_theta) / 2.0

        last_d_d_theta = -sin(radians(lasttheta)) * scaling
        last_d_theta = mid_d_theta + (mid_d_d_theta + last_d_d_theta) / 2.0
        lasttheta = midtheta + (mid_d_theta + last_d_theta) / 2.0

        self.dtheta = last_d_theta
        self.theta = lasttheta
        self.rect = Rectangle(1, 1,
                              (int(self.pivot[0] - self.swing_length * sin(radians(self.theta))),
                              int(self.pivot[1] + self.swing_length * cos(radians(self.theta)))))


