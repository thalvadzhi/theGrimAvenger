from math import sin, cos, radians
from BasicShapes import Rectangle


class Pendulum:
    def __init__(self, angle, swing_length, pivot):
        self.theta = angle
        self.d_theta = 0
        self.swing_length = swing_length
        self.pivot = pivot
        self.time = 0
        self.rect = Rectangle(1, 1,
                              (int(self.pivot[0] - self.swing_length *
                                   cos(radians(self.theta))),
                               int(self.pivot[1] + self.swing_length *
                                   sin(radians(self.theta)))))

    def recompute_angle(self):
        self.time += 1
        # modulates gravity
        scaling = 2000 / (self.swing_length ** 2)

        first_d_d_theta = -sin(radians(self.theta)) * scaling
        mid_d_theta = self.d_theta + first_d_d_theta
        mid_theta = self.theta + (self.d_theta + mid_d_theta) / 2.0

        mid_d_d_theta = -sin(radians(mid_theta)) * scaling
        mid_d_theta = self.d_theta + (first_d_d_theta + mid_d_d_theta) / 2
        mid_theta = self.theta + (self.d_theta + mid_d_theta) / 2

        mid_d_d_theta = -sin(radians(mid_theta)) * scaling
        last_d_theta = mid_d_theta + mid_d_d_theta
        last_theta = mid_theta + (mid_d_theta + last_d_theta) / 2.0

        last_d_d_theta = -sin(radians(last_theta)) * scaling
        last_d_theta = mid_d_theta + (mid_d_d_theta + last_d_d_theta) / 2.0
        last_theta = mid_theta + (mid_d_theta + last_d_theta) / 2.0

        self.d_theta = last_d_theta
        self.theta = last_theta
        self.rect = Rectangle(1, 1,
                              (int(self.pivot[0] - self.swing_length *
                                   sin(radians(self.theta))),
                               int(self.pivot[1] + self.swing_length *
                                   cos(radians(self.theta)))))
