import unittest

from pygame.math import Vector2 as Vector
import pygame

from .GUI import *
pygame.init()


def round_vector(vector, decimal=0):
    return Vector(round(vector.x, decimal), round(vector.y, decimal))


class TextBoxTest(unittest.TestCase):

    def setUp(self):
        self.text_box = TextBox(
            20, 20, Vector(0, 0), "Very long text!!!", (255, 0, 0), (None, 50))

    def test_if_avatar_is_created_correctly(self):
        self.assertEqual(self.text_box.get_width(), 20)
        self.assertEqual(self.text_box.get_width(), 20)

    def test_if_move_works_properly(self):
        expected_vertices = [round_vector(_ + Vector(5, 5))
                             for _ in self.text_box.vertices]
        self.text_box.move(Vector(5, 5))
        actual_vertices = [round_vector(_)
                           for _ in self.text_box.vertices]
        self.assertTrue(all([first == second for first, second in zip(
            expected_vertices, actual_vertices)]))

    def test_get_containing_rectangle(self):
        self.assertEqual(
            self.text_box.get_containing_rectangle(), self.text_box)


class ButtonTest(unittest.TestCase):

    def setUp(self):
        self.button = Button(
            Vector(0, 0), 100, 100, "B", (0, 0, 0), (None, 32))

    def test_if_initialized_properly(self):
        self.assertEqual(self.button.state, "normal")
        for key in self.button.states:
            self.assertTrue(key in ["normal", "active", "hover"])
        self.assertEqual(len(self.button.states.keys()), 3)
        self.assertFalse(self.button.clicked)
        self.assertEqual(self.button_type, "default")
        self.assertEqual(round_vector(self.button.position),
                         round_vector(self.button.text_box.position))

    def test_if_state_updates_properly(self):
        self.update_state(None, self.button.position)
        self.assertEqual(self.button.state, "hover")
        self.update_state(True, self.button.position)
        self.assertEqual(self.button.state, "active")
        self.update_state(False, self.button.position)
        self.assertEqual(self.button.state, "hover")
        self.assertTrue(self.button.clicked)
        self.update_state(None, self.button.position + Vector(1000, 0))
        self.assertEqual(self.button.state, "normal")
        self.update_state(True, self.button.position)
        self.assertEqual(self.button.state, "active")
        self.update_state(False, self.button.position + Vector(1000, 0))
        self.assertEqual(self.button.state, "normal")

    def test_if_move_works_properly(self):
        expected_vertices = [round_vector(_ + Vector(5, 5))
                             for _ in self.button.vertices]
        self.button.move(Vector(5, 5))
        actual_vertices = [round_vector(_)
                           for _ in self.button.vertices]
        self.assertTrue(all([first == second for first, second in zip(
            expected_vertices, actual_vertices)]))

    def test_get_containing_rectangle(self):
        self.assertEqual(
            self.button.get_containing_rectangle(), self.button)


class SliderTest(unittest.TestCase):

    def setUp(self):
        self.sliders = [Slider(Vector(0, 0), 10, (0, 100), 100, 10, 5, "B",
                               (0, 0, 0), (None, 32), 100, 100),
                        Slider(Vector(0, 0), 10, (0, 10, 100), 100, 10, 5,
                               "B", (0, 0, 0), (None, 32), 100, 100)]

    def test_if_initialized_properly(self):
        self.assertEqual(self.sliders[0].timer, 0)
        self.assertEqual(self.sliders[0].value, 10)
        self.assertEqual(self.sliders[0].state, "normal")
        for key in self.sliders[0].states:
            self.assertTrue(key in ["normal", "active", "hover"])
        self.assertEqual(len(self.sliders[0].states.keys()), 3)
        self.assertEqual(self.sliders[0].button_type, "default")

    def test_if_state_updates_properly(self):
        self.update_state(None, self.slider[0].puck.position)
        self.assertEqual(self.slider[0].state, "hover")
        self.update_state(True, self.slider[0].puck.position)
        self.assertEqual(self.slider[0].state, "active")
        self.update_state(False, self.slider[0].puck.position)
        self.assertEqual(self.slider[0].state, "hover")
        self.update_state(
            None, self.slider[0].puck.position + Vector(1000, 0))
        self.assertEqual(self.slider[0].state, "normal")
        self.update_state(True, self.slider[0].puck.position)
        self.assertEqual(self.slider[0].state, "active")
        self.update_state(None, self.slider[0].puck.position)
        self.assertEqual(self.slider[0].state, "active")
        self.assertTrue(self.slider[0].timer != 0)
        self.update_state(
            False, self.slider[0].puck.position + Vector(1000, 0))
        self.assertEqual(self.slider[0].state, "normal")

    def test_if_move_works_properly(self):
        expected_vertices = [Vector(round(_.x), round(_.y)) + Vector(5, 5)
                             for _ in self.button.vertices]
        self.button.move(Vector(5, 5))
        actual_vertices = [Vector(round(_.x), round(_.y))
                           for _ in self.button.vertices]
        self.assertTrue(all([first == second for first, second in zip(
            expected_vertices, actual_vertices)]))

    def test_get_containing_rectangle(self):
        self.assertEqual(
            self.button.get_containing_rectangle(), self.button)


class CheckboxTest(unittest.TestCase):

    def setUp(self):
        self.checkbox = Checkbox(Vector(0, 0), True, 100, 10, "B",
                                 (0, 0, 0), (None, 32), 100, 100)

    def test_if_initialized_properly(self):
        self.assertEqual(self.checkbox.state, "checked")
        for key in self.checkbox.states:
            self.assertTrue(key in ["checked", "checked_hover",
                                    "unchecked_hover", "unchecked"])
        self.assertEqual(len(self.checkbox.states.keys()), 4)
        self.assertEqual(self.checkbox_type, "default")
        self.assertEqual(round_vector(self.button.position),
                         round_vector(self.button.text_box.position))

    def test_if_state_updates_properly(self):
        self.update_state(None, self.button.position)
        self.assertEqual(self.button.state, "hover")
        self.update_state(True, self.button.position)
        self.assertEqual(self.button.state, "active")
        self.update_state(False, self.button.position)
        self.assertEqual(self.button.state, "hover")
        self.assertTrue(self.button.clicked)
        self.update_state(None, self.button.position + Vector(1000, 0))
        self.assertEqual(self.button.state, "normal")
        self.update_state(True, self.button.position)
        self.assertEqual(self.button.state, "active")
        self.update_state(False, self.button.position + Vector(1000, 0))
        self.assertEqual(self.button.state, "normal")

    def test_if_move_works_properly(self):
        expected_vertices = [round_vector(_ + Vector(5, 5))
                             for _ in self.button.vertices]
        self.button.move(Vector(5, 5))
        actual_vertices = [round_vector(_)
                           for _ in self.button.vertices]
        self.assertTrue(all([first == second for first, second in zip(
            expected_vertices, actual_vertices)]))

    def test_get_containing_rectangle(self):
        self.assertEqual(
            self.button.get_containing_rectangle(), self.button)

if __name__ == "__main__":
    unittest.main()
