import math


class Point:
    def __init__(self, x, y, angle=0, distance=0):
        self.x = x
        self.y = y
        self.angle = angle
        self.distance = distance

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    @classmethod
    def get_intersection(cls, ray, obstacle):
        # ray in parametric
        r_px = ray.point1.x
        r_py = ray.point1.y
        r_dx = ray.point2.x - ray.point1.x
        r_dy = ray.point2.y - ray.point1.y

        # obstacle in parametric
        s_px = obstacle.point1.x
        s_py = obstacle.point1.y
        s_dx = obstacle.point2.x - obstacle.point1.x
        s_dy = obstacle.point2.y - obstacle.point1.y

        r_mag = math.sqrt(r_dx * r_dx + r_dy * r_dy)
        s_mag = math.sqrt(s_dx * s_dx + s_dy * s_dy)
        try:
            if r_dx / r_mag == s_dx / s_mag and r_dy / r_mag == s_dy / s_mag:
                # Unit vectors are the same.
                return None

            t2 = (r_dx * (s_py-r_py) + r_dy * (r_px-s_px))\
                / (s_dx * r_dy - s_dy * r_dx)
            t1 = (s_px + s_dx * t2 - r_px) / r_dx
        except ZeroDivisionError:
            return None

        if t1 < 0:
            return None
        if t2 < 0 or t2 > 1:
            return None
        # Return the POINT OF INTERSECTION
        return Point(r_px + r_dx * t1, r_py + r_dy * t1, 0, t1)

    def is_between_points(self, target):
        dot_product = (target.x - self.point1.x) * \
                      (self.point2.x - self.point1.x) + \
                      (target.y - self.point1.y) * \
                      (self.point2.y - self.point1.y)
        if dot_product < 0:
            return False

        squared_length = (self.point2.x - self.point1.x) ** 2 + \
                         (self.point2.y - self.point2.y) ** 2
        if dot_product > squared_length:
            return False
        return True


class LightSource:
    def __init__(self, x, y, obstacles):
        self.x = x
        self.y = y
        self.obstacles = obstacles
        self.segments = []
        self.generate_all_walls()
        self.uniquify()

    def update_obstacles(self, obstacles):
        self.segments = []
        self.obstacles = obstacles
        self.generate_all_walls()
        self.uniquify()

    def update_light_source_position(self, x, y):
        self.x = x
        self.y = y

    def generate_walls(self, obstacle):
        # takes obstacle as a list of coordinates
        index = 0
        sides = []
        while index < len(obstacle) - 1:
            point1 = obstacle[index]
            point2 = obstacle[index + 1]
            sides.append(Line(point1, point2))
            index += 1
        sides.append(Line(obstacle[0], obstacle[3]))
        return sides

    def generate_all_walls(self):
        # will generate the lines of the sides
        for obstacle in self.obstacles:
            self.segments.extend(self.generate_walls(obstacle))

    def uniquify(self):
        # take only the unique points
        self.obstacles = [segment for obstacle in self.obstacles
                          for segment in obstacle]
        self.obstacles = list(set(self.obstacles))

    def get_all_angles(self):
        unique_angles = []
        for point in self.obstacles:
            angle = math.atan2(point.y - self.y, point.x - self.x)
            point.angle = angle
            unique_angles.append(angle - 0.00001)
            unique_angles.append(angle)
            unique_angles.append(angle + 0.00001)
        return unique_angles

    def cast(self):
        intersections = []
        unique_angles = self.get_all_angles()
        light = Point(self.x, self.y)
        for angle in unique_angles:
            dx = math.cos(angle)
            dy = math.sin(angle)

            ray = Line(light, Point(self.x + dx, self.y + dy))

            closest = None
            for segment in self.segments:
                intersection = Line.get_intersection(ray, segment)
                if intersection is None:
                    continue
                if closest is None or intersection.distance < closest.distance:
                    closest = intersection

            if closest is None:
                continue

            closest.angle = angle
            intersections.append(closest)

        intersections.sort(key=lambda point: point.angle)

        return self.to_tuple(intersections)

    def to_tuple(self, intersections):
        visibility = []
        for intersection in intersections:
            visibility.append((intersection.x, intersection.y))
        return visibility
