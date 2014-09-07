import unittest
from itertools import combinations

from pygame.math import Vector2 as Vector

from VectorMath import Line, check_if_parallel
from BasicShapes import *


class RigitBodyTest(unittest.TestCase):

    POSITIONS = [Vector(0, 0), Vector(250, 250), Vector(-20, -20),
                 Vector(-33, 46), Vector(56, -12)]

    DENSITIES = [0, 20, 30, 12, 45]

    def setUp(self):
        self.rigit_bodies = [
            RigitBody(RigitBodyTest.POSITIONS[_])
            for _ in range(0, len(RigitBodyTest.POSITIONS))]

    def test_if_hashes_are_unique(self):
        for pair in combinations(self.rigit_bodies, 2):
            self.assertNotEqual(pair[0].__hash__(), pair[1].__hash__())

    def test_properties(self):
        for index in range(0, len(self.rigit_bodies)):
            self.assertEqual(self.rigit_bodies[index].position,
                             RigitBodyTest.POSITIONS[index])
            self.assertEqual(self.rigit_bodies[index].direction,
                             Vector(1, 0))

    def test_other_overloaded_methods(self):
        for index in range(0, len(self.rigit_bodies)):
            self.assertEqual(str(self.rigit_bodies[index]), "RigitBody")

    def test_if_position_in_world_and_on_body_calculate_properly(self):
        point_on_body = Vector(0, 1)
        for index in range(0, len(self.rigit_bodies)):
            self.assertEqual(
                self.rigit_bodies[index].position_in_world(point_on_body),
                RigitBodyTest.POSITIONS[index] + point_on_body)
            self.assertEqual(
                self.rigit_bodies[index].position_on_body(
                    RigitBodyTest.POSITIONS[index] + point_on_body),
                point_on_body)

    def test_rotation(self):
        for index in range(0, len(self.rigit_bodies)):
            self.rigit_bodies[index].rotate(index)
            self.assertEqual(self.rigit_bodies[index].direction,
                             Vector(1, 0).rotate(index))

    def test_translation(self):
        for index in range(0, len(self.rigit_bodies)):
            self.rigit_bodies[index].move(Vector(index, index))
            self.assertEqual(self.rigit_bodies[index].position,
                             self.POSITIONS[index] + Vector(index, index))

    def test_if_avatars_are_loaded_properly(self):
        self.rigit_bodies[1].load_avatar(r"Ragdolls/Batman/dlvk.png")
        self.assertEqual(self.rigit_bodies[1].image_master, None)

    def test_if_avatars_are_scaled_properly(self):
        self.rigit_bodies[1].scale_avatar(2, 1)
        self.assertEqual(self.rigit_bodies[1].image_master, None)

    def test_if_rotate_around_works_properly(self):
        body = RigitBody(Vector(250, 250))
        body.rotate_around(Vector(0, 1), 90)
        self.assertEqual(body.direction, Vector(1, 0).rotate(90))
        self.assertEqual(Vector(
            round((Vector(0, 1).rotate(90) + body.position).x),
            round((Vector(0, 1).rotate(90) + body.position).y)),
            Vector(250, 251))

    def test_if_pull_on_anchor_works_properly(self):
        body = RigitBody(Vector(250, 250))
        body.pull_on_anchor(Vector(0, 1), Vector(1, -1))
        self.assertEqual(Vector(
            round(body.position_in_world(Vector(0, 1)).x),
            round(body.position_in_world(Vector(0, 1)).y)),
            Vector(250, 251))


class CircleTest(unittest.TestCase):

    RADIUSES = [10, 20, 30]

    POSITIONS = [Vector(0, 0), Vector(250, 250), Vector(-20, -20)]

    DENSITIES = [0, 20, 30]

    def setUp(self):
        self.circles = [Circle(
            CircleTest.RADIUSES[_], CircleTest.POSITIONS[_],
            CircleTest.DENSITIES[_])
            for _ in range(0, len(CircleTest.POSITIONS))]

    def test_surface_calculating(self):
        self.assertEqual(
            round(self.circles[0].calculate_surface(), 2), 314.16)
        self.assertEqual(
            round(self.circles[1].calculate_surface(), 2), 1256.64)
        self.assertEqual(
            round(self.circles[2].calculate_surface(), 2), 2827.43)

    def test_if_mass_is_properly_calculated(self):
        self.assertEqual(self.circles[0].mass, 0)
        self.assertEqual(round(self.circles[1].mass, 1), 25132.7)
        self.assertEqual(round(self.circles[2].mass, 1), 84823.0)

    def test_if_hashes_are_unique(self):
        for pair in combinations(self.circles, 2):
            self.assertNotEqual(pair[0].__hash__(), pair[1].__hash__())

    def test_properties(self):
        for index in range(0, len(self.circles)):
            self.assertEqual(self.circles[index].radius,
                             CircleTest.RADIUSES[index])

    def test_is_point_in_body_method(self):
        self.assertTrue(
            self.circles[0].is_point_in_body(self.circles[0].position))
        self.assertFalse(self.circles[0].is_point_in_body(
            self.circles[0].position + Vector(
                self.circles[0].radius + 10, 0)))

    def test_other_overloaded_methods(self):
        self.assertTrue(self.circles[0] == self.circles[0])
        self.assertFalse(self.circles[0] == self.circles[1])

    def test_get_SAT_axis(self):
        self.assertEqual(self.circles[0].get_SAT_axis(), [])

    def test_collide_circle(self):
        result = self.circles[0].collide_circle(self.circles[1])
        self.assertFalse(result[0])
        result = self.circles[0].collide_circle(self.circles[2])
        self.assertTrue(result[0])
        self.assertEqual(
            Vector(round(result[1].x), round(result[1].y)), Vector(-8, -8))

    def test_get_SAT_projections(self):
        result = self.circles[0].get_SAT_projections(
            Line(Vector(0, 0), Vector(1, 0)))
        self.assertEqual(round(result[0]), -10)
        self.assertEqual(round(result[1]), 10)


class RectangleTest(unittest.TestCase):

    def setUp(self):
        self.rectangle = Rectangle(10, 10, Vector(0, 0), 1)

    def test_surface_calculating(self):
        self.assertEqual(round(self.rectangle.calculate_surface()), 100)

    def test_if_mass_is_properly_calculated(self):
        self.assertEqual(round(self.rectangle.mass), 100)

    def test_if_hashes_are_unique(self):
        body = Rectangle(10, 10, Vector(0, 0), 1)
        self.assertNotEqual(body.__hash__(), self.rectangle.__hash__())

    def test_properties(self):
        self.assertEqual(self.rectangle.width, 10)
        self.assertEqual(self.rectangle.height, 10)

    def test_is_point_in_body_method(self):
        self.assertTrue(
            self.rectangle.is_point_in_body(self.rectangle.position))
        self.assertFalse(self.rectangle.is_point_in_body(Vector(100, 0)))

    def test_other_overloaded_methods(self):
        body = Rectangle(10, 10, Vector(1, 0), 1)
        self.assertTrue(self.rectangle == self.rectangle)
        self.assertFalse(self.rectangle == body)

    def test_get_SAT_axis(self):
        result = self.rectangle.get_SAT_axis()
        self.assertTrue(2 == len(result))
        self.assertTrue(check_if_parallel(result[0].direction,
                                          self.rectangle.vertices[1] -
                                          self.rectangle.vertices[0]))
        self.assertTrue(check_if_parallel(result[1].direction,
                                          self.rectangle.vertices[2] -
                                          self.rectangle.vertices[1]))

    def test_collides_rectangle(self):
        self.assertTrue(self.rectangle.collides_rectangle(
            Rectangle(10, 10, Vector(5, 0), 1)))
        self.assertFalse(self.rectangle.collides_rectangle(
            Rectangle(10, 10, Vector(100, 0), 1)))

    def test_get_SAT_projections(self):
        result = self.rectangle.get_SAT_projections(
            Line(Vector(0, 0), Vector(1, 0)))
        self.assertEqual(round(result[0]), -5)
        self.assertEqual(round(result[1]), 5)

    def test_sync_position(self):
        self.rectangle.move(Vector(5, 5))
        self.rectangle.sync_position()
        vertices = [Vector(round(_.x), round(_.y))
                    for _ in self.rectangle.vertices]
        self.assertEqual(vertices[0], Vector(0, 10))
        self.assertEqual(vertices[1], Vector(10, 10))
        self.assertEqual(vertices[2], Vector(10, 0))
        self.assertEqual(vertices[3], Vector(0, 0))


class TriangleTest(unittest.TestCase):

    def setUp(self):
        self.triangles = [Triangle([Vector(0, 0), Vector(1, 0), Vector(0, 1)],
                                   Vector(0, 0), 1),
                          Triangle([3, 4, 5], Vector(0, 0), 1)]

    def test_surface_calculating(self):
        self.assertEqual(round(self.triangles[0].calculate_surface(), 1), 0.5)
        self.assertEqual(round(self.triangles[1].calculate_surface()), 6)

    def test_if_mass_is_properly_calculated(self):
        self.assertEqual(round(self.triangles[0].mass, 1), 0.5)
        self.assertEqual(round(self.triangles[1].mass), 6)

    def test_if_hashes_are_unique(self):
        self.assertNotEqual(self.triangles[0].__hash__(),
                            self.triangles[1].__hash__())

    def test_is_point_in_body_method(self):
        self.assertTrue(
            self.triangles[0].is_point_in_body(self.triangles[0].position))
        self.assertFalse(self.triangles[0].is_point_in_body(Vector(100, 100)))
        self.assertTrue(
            self.triangles[1].is_point_in_body(self.triangles[1].position))
        self.assertFalse(self.triangles[1].is_point_in_body(Vector(100, 100)))

    def test_other_overloaded_methods(self):
        self.assertTrue(self.triangles[0] == self.triangles[0])
        self.assertFalse(self.triangles[0] == self.triangles[1])

    #def test_get_SAT_axis(self):
    #    result = self.rectangle.get_SAT_axis()
    #    self.assertTrue(2 == len(result))
    #    self.assertTrue(check_if_parallel(result[0].direction,
    #                                      self.rectangle.vertices[1] -
    #                                      self.rectangle.vertices[0]))
    #    self.assertTrue(check_if_parallel(result[1].direction,
    #                                      self.rectangle.vertices[2] -
    #                                      self.rectangle.vertices[1]))

    #def test_get_SAT_projections(self):
    #    result = self.triangles.get_SAT_projections(
    #        Line(Vector(0, 0), Vector(1, 0)))
    #    self.assertEqual(round(result[0]), -5)
    #    self.assertEqual(round(result[0]), 5)

    def test_calculate_edges(self):
        edge_lenghts = {'AB': 1.0, 'AC': 1.0, 'BC': 1.4}
        self.triangles[0].calculate_edges()
        for edge, length in self.triangles[0].edge_lenghts.items():
            self.assertEqual(round(length, 1), edge_lenghts[edge])

    def test_sync_centroid(self):
        vertices = {'A': Vector(-0.3, -0.3), 'B': Vector(0.7, -0.3),
                    'C': Vector(-0.3, 0.7)}
        self.triangles[0].sync_centroid()
        for key, vertex in self.triangles[0].generic_vertices.items():
            self.assertEqual(
                Vector(round(vertex.x, 1), round(vertex.y, 1)), vertices[key])

    def test_calculate_vertices(self):
        vertices = {"A": Vector(0, 0), "B": Vector(1, 0), "C": Vector(0, 1)}
        self.triangles[0].calculate_vertices()
        for key, vertex in self.triangles[0].vertices.items():
            self.assertEqual(
                Vector(round(vertex.x), round(vertex.y)), vertices[key])

    def test_sync_position(self):
        vertices = {'A': Vector(-0.3, -0.3), 'B': Vector(0.7, -0.3),
                    'C': Vector(-0.3, 0.7)}
        self.triangles[0].sync_position()
        for key, vertex in self.triangles[0].vertices.items():
            self.assertEqual(
                Vector(round(vertex.x, 1), round(vertex.y, 1)), vertices[key])

if __name__ == "__main__":
    unittest.main()
