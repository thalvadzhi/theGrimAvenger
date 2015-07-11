import unittest

from pygame.math import Vector2 as Vector
import pygame

from gui import *
from control import Control
pygame.init()


def round_vector(vector, decimal=0):
    return Vector(round(vector.x, decimal), round(vector.y, decimal))


class SoundEffectTest(unittest.TestCase):

    @classmethod
    def setUpClass(ls):
        SoundEffect.play_music("menu.mp3")

    def SetUp(self):
        self.sound = SoundEffect("button_default.wav")

    def test_if_sounds_are_cached(self):
        self.assertNotEqual(len(SoundEffect.LOADED), 0)
        self.assertIn("button_default.wav", SoundEffect.LOADED)

    def test_reset_volume(self):
        self.sound.volume = 40
        self.sound.reset_volume()
        self.assertAlmostEqual(self.sound.sound.get_volume, 40 / 100)

    def test_reset_volume_with_zero(self):
        self.sound.volume = 0
        self.sound.reset_volume()
        self.assertEqual(self.sound.sound.get_volume, 0)

    def test_set_music_volume(self):
        SoundEffect.set_music_volume(40)
        self.assertAlmostEqual(pygame.mixer.music.get_volume(), 40 / 100)

    def test_set_music_volume_with_zero(self):
        SoundEffect.set_music_volume(0)
        self.assertEqual(pygame.mixer.music.get_volume(), 0)

    def test_if_play_fixes_volume(self):
        previous_volume = self.sound.volume
        self.sound.volume = (self.sound.volume + 50) // 2
        self.sound.play()
        self.assertEqual(self.sound.volume, previous_volume)


class TextBoxTest(unittest.TestCase):

    def setUp(self):
        self.text_box = TextBox(
            20, 20, Vector(0, 0), "Very long text!!!", (255, 0, 0), (None, 50))

    def test_update_state_does_nothing(self):
        self.text_box.update_state()
        self.assertEqual(self.text_box.width, 20)
        self.assertEqual(self.text_box.width, 20)
        self.assertEqual(self.text_box.text, "Very long text!!!")
        self.assertEqual(self.text_box.text_font, (None, 50))
        self.assertEqual(self.text_box.text_colour, (255, 0, 0))
        self.assertAlmostEqual(self.text_box.position[0], 0)
        self.assertAlmostEqual(self.text_box.position[1], 0)

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

    def test_move_puck_out_of_left_boundary(self):
        slider = self.sliders[0]
        slider.move_puck(Vector(-5000, -34))
        self.assertAlmostEqual(
            slider.puck.position.x, self.position.x - self.width / 2)
        self.assertAlmostEqual(slider.puck.position.y, self.position.y)

    def test_move_puck_out_of_right_boundary(self):
        slider = self.sliders[0]
        slider.move_puck(Vector(5000, -3))
        self.assertAlmostEqual(
            slider.puck.position.x, self.position.x + self.width / 2)
        self.assertAlmostEqual(slider.puck.position.y, self.position.y)

    def test_value_after_move_puck(self):
        slider = self.sliders[0]
        slider_on_list = Slider(
            Vector(0, 0), 10, [1, 2, 3], 100, 10, 5, "B",
            (0, 0, 0), (None, 32), 100, 100)
        slider.move_puck(Vector(-5000, -34))
        self.assertEqual(slider.value, 0)
        slider.move_puck(Vector(slider.width // 2 + 15, -34))
        self.assertEqual(slider.value, slider.width // 2 + 15)
        slider_on_list.move_puck(Vector(-5000, -34))
        self.assertEqual(slider_on_list.value, 1)
        slider_on_list.move_puck(Vector(slider.width // 2 + 4, -34))
        self.assertEqual(slider_on_list.value, 2)
        slider_on_list.move_puck(Vector(slider.width // 2 - 10, -34))
        self.assertEqual(slider_on_list.value, 3)

    def test_value_setter(self):
        slider = Slider(Vector(0, 0), 10, [1, 2, 3], 100, 10, 5, "B",
                        (0, 0, 0), (None, 32), 100, 100)
        slider.value = 2
        self.assertAlmostEqual(slider.puck.position.x, slider.position.x)
        slider.value = 1
        self.assertAlmostEqual(
            slider.puck.position.x, slider.position.x - slider.width // 2)
        slider.value = 3
        self.assertAlmostEqual(
            slider.puck.position.x, slider.position.x + slider.width // 2)


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
