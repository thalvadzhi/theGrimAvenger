import unittest

from pygame.math import Vector2 as Vector
import pygame

from gui import *
from control import Control
pygame.init()


def round_vector(vector, decimal=0):
    return Vector(round(vector.x, decimal), round(vector.y, decimal))


class TextBoxTest(unittest.TestCase):

    def setUp(self):
        self.text_box = TextBox(
            20, 20, Vector(0, 0), "Very long text!!!", (255, 0, 0), (None, 50))

    def test_if_avatar_is_created_correctly(self):
        self.assertEqual(self.text_box.width, 20)
        self.assertEqual(self.text_box.width, 20)

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
        self.assertEqual(self.button.button_type, "default")
        self.assertEqual(round_vector(self.button.position),
                         round_vector(self.button.text_box.position))

    def test_if_state_updates_properly(self):
        self.button.update_state(self.button.position, None)
        self.assertEqual(self.button.state, "hover")
        self.button.update_state(self.button.position, True)
        self.assertEqual(self.button.state, "active")
        self.button.update_state(self.button.position, False)
        self.assertEqual(self.button.state, "hover")
        self.assertTrue(self.button.clicked)
        self.button.update_state(self.button.position + Vector(1000, 0), None)
        self.assertEqual(self.button.state, "normal")
        self.button.update_state(self.button.position, True)
        self.assertEqual(self.button.state, "active")
        self.button.update_state(self.button.position + Vector(1000, 0), False)
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
        self.assertEqual(self.sliders[0].slider_type, "default")

    def test_if_state_updates_properly(self):
        self.sliders[0].update_state(self.sliders[0].puck.position, None)
        self.assertEqual(self.sliders[0].state, "hover")
        self.sliders[0].update_state(self.sliders[0].puck.position, True)
        self.assertEqual(self.sliders[0].state, "active")
        self.sliders[0].update_state(self.sliders[0].puck.position, False)
        self.assertEqual(self.sliders[0].state, "hover")
        self.sliders[0].update_state(
            self.sliders[0].puck.position + Vector(1000, 0), None)
        self.assertEqual(self.sliders[0].state, "normal")
        self.sliders[0].update_state(self.sliders[0].puck.position, True)
        self.assertEqual(self.sliders[0].state, "active")
        self.sliders[0].update_state(self.sliders[0].puck.position, None)
        self.assertEqual(self.sliders[0].state, "active")
        self.assertTrue(self.sliders[0].timer != 0)
        self.sliders[0].update_state(
            self.sliders[0].puck.position + Vector(1000, 0), False)
        self.assertEqual(self.sliders[0].state, "normal")


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
        self.assertEqual(self.checkbox.checkbox_type, "default")


class MenuTest(unittest.TestCase):

    def setUp(self):
        Menu.init_menus(Control())

    def test_if_menues_are_correctly_initialized(self):
        for menu in ["welcome_menu", "options_menu", "sound_menu",
                     "video_menu", "new_game_menu", "load_game_menu",
                     "save_game_menu", "pause_menu"]:
            self.assertTrue(menu in Menu.MENUS.keys())


if __name__ == "__main__":
    unittest.main()
