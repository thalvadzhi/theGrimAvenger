from os import listdir

import pygame
from pygame.math import Vector2 as Vector

from BasicShapes import Rectangle, Circle

GUI_SETTINGS = {
    "fps": 60,
    "resolution": (1366, 768),
    "fullscreen": False,
}

SOUND_SETTINGS = {
    "music": 50,
    "effects": 50
}

RESOLUTIONS = [(1280, 1024), (1366, 768), (1600, 1024),
               (1600, 1200), (1920, 1080), (1920, 1200)]

class SoundEffect:
    """
    Fix settings not being loaded/saved maybe not using global SOUND_SETTINGS
    """
    LOADED = {}

    def __init__(self, sound):
        if sound in SoundEffect.LOADED:
            self.sound = SoundEffect.LOADED[sound]
        else:
            self.sound = pygame.mixer.Sound(
                r"../Files/Sounds/{0}".format(sound))
            SoundEffect.LOADED[sound] = self.sound
        self.volume = SOUND_SETTINGS["effects"]
        self.reset_volume()

    def reset_volume(self):
        if self.volume is 0:
            self.sound.set_volume(self.volume)
        else:
            self.sound.set_volume(self.volume / 100)

    @classmethod
    def set_music_volume(cls, volume):
        SOUND_SETTINGS["music"] = volume
        if volume is 0:
            pygame.mixer.music.set_volume(volume)
        else:
            pygame.mixer.music.set_volume(volume / 100)

    @classmethod
    def play_music(cls, path):
        pygame.mixer.music.load(r"../Files/Sounds/{0}".format(path))
        pygame.mixer.music.play(-1)

    def play(self):
        if self.volume != SOUND_SETTINGS["effects"]:
            self.volume = SOUND_SETTINGS["effects"]
            self.reset_volume()
        self.sound.play()

class TextBox(Rectangle):

    def __init__(self, width, height, position, text, text_colour, text_font,
                 background=None):
        Rectangle.__init__(self, width, height, position)
        self.text = text
        self.text_colour = text_colour
        self.text_font = text_font
        self.background = background
        self.create_text_avatar()

    def get_containing_rectangle(self):
        return self

    def move(self, translation):
        Rectangle.move(self, translation)
        self.sync_position()

    def update_state(self, mouse_position, event):
        pass

    def create_text_avatar(self):
        self.text_avatar = pygame.font.Font(*self.text_font).render(
            self.text, 20, self.text_colour)
        if self.text_avatar.get_width() > self.width or \
           self.text_avatar.get_height() > self.height:
            self.text_avatar = pygame.transform.scale(
                self.text_avatar, (int(self.width), int(self.height)))

    def draw(self, surface):
        if self.background is not None:
            surface.blit(self.background, self.vertices[3])
        surface.blit(self.text_avatar, self.position - Vector(
            self.text_avatar.get_width(), self.text_avatar.get_height()) / 2)


class Button(Rectangle):

    def __init__(self, position, width, height, text, text_colour,
                 text_font, button_type="default"):
        Rectangle.__init__(self, width, height, position)
        self.states = {}
        for state in ["active", "hover", "normal"]:
            self.load_avatar(
                r"GUI/Button/{0}/{1}.png".format(button_type, state))
            self.scale_avatar(self.width, self.height)
            self.states[state] = self.image_master
        self.state = "normal"
        self.clicked = False
        self.sound_effect = SoundEffect(r"button_{0}.wav".format(button_type))
        self.text_box = TextBox(width, height, position, text,
                                text_colour, text_font)
        self.button_type = button_type

    def move(self, translation):
        Rectangle.move(self, translation)
        self.sync_position()
        self.text_box.move(translation)

    def get_containing_rectangle(self):
        return self

    def update_state(self, mouse_position, event):
        mouse_on_button = self.is_point_in_body(mouse_position)
        if self.state is "active":
            if not event:
                if mouse_on_button:
                    self.state = "hover"
                    self.clicked = True
                    self.sound_effect.play()
                else:
                    self.state = "normal"
        elif self.state is "hover":
            if event and mouse_on_button:
                self.state = "active"
            elif not mouse_on_button:
                self.state = "normal"
        else:
            if event and mouse_on_button:
                self.state = "active"
            elif mouse_on_button:
                self.state = "hover"
        self.image_master = self.states[self.state]

    def draw(self, surface):
        self.display_avatar(surface)
        self.text_box.draw(surface)


class Slider(Rectangle):

    def __init__(self, position, value, values, width, height, puck_radius,
                 text, text_colour, text_font, text_box_width, text_box_height,
                 slider_type="default"):
        self.__value = value
        self.values = values
        self.timer = 0
        position = position + Vector(0, text_box_height / 2)
        Rectangle.__init__(self, width, height, position)
        self.puck = Circle(puck_radius, position)
        self.states = {}
        for state in ["active", "hover", "normal"]:
            self.puck.load_avatar(
                r"GUI/Slider/{0}/{1}.png".format(slider_type, state))
            self.puck.scale_avatar(
                self.puck.radius * 2, self.puck.radius * 2)
            self.states[state] = self.puck.image_master
        self.sound_effect = SoundEffect(r"slider_{0}.wav".format(slider_type))
        self.state = "normal"
        self.text_box = TextBox(
            text_box_width, text_box_height, position +
            Vector(0, -max(self.puck.radius, height / 2) -
                   text_box_height / 2), text,
            text_colour, text_font)
        self.left_fill = (253, 238, 0)
        self.right_fill = (0, 0, 0)
        self.slider_type = slider_type
        self.sync_puck()

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value
        self.sync_puck()

    def move(self, translation):
        Rectangle.move(self, translation)
        self.sync_position()
        self.puck.move(translation)
        self.text_box.move(translation)

    def get_containing_rectangle(self):
        width = max(self.width, self.text_box.width)
        height = max(self.height, self.puck.radius * 2) + \
            self.text_box.height
        return Rectangle(width, height, self.position +
                         Vector(0, -self.text_box.height / 2))

    def update_state(self, mouse_position, event):
        mouse_on_puck = self.puck.is_point_in_body(mouse_position)
        if self.state is "active":
            if event is False:
                if mouse_on_puck:
                    self.state = "hover"
                else:
                    self.state = "normal"
            elif event is None:
                self.move_puck(
                    Vector(mouse_position.x - self.puck.position.x, 0))
                self.value_text_box = TextBox(
                    self.text_box.width, self.text_box.height,
                    self.text_box.position, str(self.value),
                    self.text_box.text_colour, self.text_box.text_font)
                self.timer = pygame.time.get_ticks() + 1000
        elif self.state is "hover":
            if event and mouse_on_puck:
                self.state = "active"
                self.sound_effect.play()
            elif not mouse_on_puck:
                self.state = "normal"
        else:
            if event and mouse_on_puck:
                self.state = "active"
                self.sound_effect.play()
            elif mouse_on_puck:
                self.state = "hover"
        self.puck.image_master = self.states[self.state]

    def move_puck(self, translation):
        self.puck.move(translation)
        if self.puck.position.x < self.position.x - self.width / 2:
            self.puck.move(Vector(self.position.x - self.width / 2 -
                                  self.puck.position.x, 0))
        elif self.puck.position.x > self.position.x + self.width / 2:
            self.puck.move(Vector(self.position.x + self.width / 2 -
                                  self.puck.position.x, 0))
        if len(self.values) == 2:
            self.__value = self.values[0] + (self.values[1] - self.values[0]) \
                * ((self.puck.position.x - self.position.x +
                    self.width / 2) / self.width)
            self.__value = round(self.__value)
        else:
            step = round((len(self.values) - 1) *
                         ((self.puck.position.x - self.position.x +
                           self.width / 2) / self.width))
            self.__value = self.values[step]
        self.sync_puck()

    def sync_puck(self):
        portion = 0
        if len(self.values) == 2:
            portion = (self.value - self.values[0]) / (
                self.values[1] - self.values[0])
        else:
            step = self.values.index(self.value)
            portion = (step) / (len(self.values) - 1)
        self.puck.move(Vector(self.position.x - self.width / 2 +
                              self.width * portion -
                              self.puck.position.x, 0))

    def draw(self, surface):
        pygame.draw.polygon(surface, self.right_fill, self.vertices)
        pygame.draw.polygon(
            surface, self.left_fill, [
                self.puck.position - Vector(0, self.height / 2),
                self.puck.position + Vector(0, self.height / 2),
                self.vertices[0], self.vertices[3]])
        self.puck.display_avatar(surface)
        if pygame.time.get_ticks() < self.timer:
            self.value_text_box.draw(surface)
        else:
            self.text_box.draw(surface)


class Checkbox(Rectangle):

    def __init__(self, position, value, width, height, text, text_colour,
                 text_font, text_box_width, text_box_height,
                 checkbox_type="default"):
        Rectangle.__init__(self, width, height, position + Vector(
            -text_box_width / 2, 0))
        self.states = {}
        for state in ["checked", "unchecked",
                      "checked_hover", "unchecked_hover"]:
            self.load_avatar(
                r"GUI/Checkbox/{0}/{1}.png".format(checkbox_type, state))
            self.scale_avatar(self.width, self.height)
            self.states[state] = self.image_master
        if value:
            self.state = "checked"
        else:
            self.state = "unchecked"
        self.sound_effect = SoundEffect(r"checkbox_{0}.wav".format(checkbox_type))
        self.text_box = TextBox(
            text_box_width, text_box_height, self.position +
            Vector((self.width + text_box_width) / 2, 0),
            text, text_colour, text_font)
        self.checkbox_type = checkbox_type

    @property
    def value(self):
        if self.state is "checked" or self.state is "checked_hover":
            return True
        return False

    @value.setter
    def value(self, value):
        if value:
            if self.state[-5:] is "hover":
                self.state = "checked_hover"
            else:
                self.state = "checked"
        else:
            if self.state[-5:] is "hover":
                self.state = "unchecked_hover"
            else:
                self.state = "unchecked"

    def move(self, translation):
        Rectangle.move(self, translation)
        self.sync_position()
        self.text_box.move(translation)

    def get_containing_rectangle(self):
        width = self.width + self.text_box.width
        height = max(self.height, self.text_box.height)
        return Rectangle(width, height, self.position +
                         Vector(self.text_box.width / 2, 0))

    def update_state(self, mouse_position, event):
        mouse_on_checkbox = self.is_point_in_body(mouse_position)
        if event:
            if mouse_on_checkbox:
                if self.state is "checked_hover" or self.state is "checked":
                    self.state = "unchecked_hover"
                    self.sound_effect.play()
                else:
                    self.state = "checked_hover"
                    self.sound_effect.play()
        else:
            if mouse_on_checkbox:
                if self.state is "checked":
                    self.state = "checked_hover"
                elif self.state is "unchecked":
                    self.state = "unchecked_hover"
            else:
                if self.state is "checked_hover":
                    self.state = "checked"
                elif self.state is "unchecked_hover":
                    self.state = "unchecked"

    def draw(self, surface):
        self.image_master = self.states[self.state]
        self.display_avatar(surface)
        self.text_box.draw(surface)


class Menu(Rectangle):

    MENUS = {}

    def __init__(self, width, height, position, title, title_colour,
                 title_font, title_box_width, title_box_height,
                 menu_type="default"):
        Rectangle.__init__(self, width, height, position)
        self.load_avatar(r"GUI/Menu/{0}.jpg".format(menu_type))
        self.elements = [TextBox(
            title_box_width, title_box_height,
            Vector(width / 2, title_box_height / 2 + 10),
            title, title_colour, title_font)]
        self.frame = ((0, 0, 0), 10)
        self.menu_type = menu_type

    def add_element(self, spacing, element_type, *args):
        previous = self.elements[-1].get_containing_rectangle()
        self.elements.append(element_type(previous.position, *args))
        current = self.elements[-1].get_containing_rectangle()
        self.elements[-1].move(Vector(0, previous.height / 2 +
                                      current.height / 2 + spacing))

    def handle_input(self, control):
        for event in control.mouse_input:
            if event[0] == 1:
                for element in self.elements:
                    element.update_state(event[1] - self.vertices[3], event[2])
        for element in self.elements:
            element.update_state(
                control.cursor_location - self.vertices[3], None)

    def reset_menu_buttons(self):
        for element in self.elements:
            if isinstance(element, Button):
                element.clicked = False

    @classmethod
    def init_menus(cls, control):
        screen_centre = Vector(control.gui_settings["resolution"]) / 2

        welcome_menu = cls(600, 380, screen_centre, "Welcome",
                           (0, 0, 0), (None, 50), 400, 50)
        welcome_menu.add_element(
            20, Button, 400, 50, "NEW GAME", (0, 0, 0), (None, 50))
        welcome_menu.add_element(
            20, Button, 400, 50, "LOAD", (0, 0, 0), (None, 50))
        welcome_menu.add_element(
            20, Button, 400, 50, "OPTIONS", (0, 0, 0), (None, 50))
        welcome_menu.add_element(
            20, Button, 400, 50, "QUIT", (0, 0, 0), (None, 50))
        cls.MENUS["welcome_menu"] = welcome_menu

        options_menu = cls(600, 310, screen_centre, "OPTIONS",
                           (0, 0, 0), (None, 50), 400, 50)
        options_menu.add_element(
            20, Button, 400, 50, "SOUND", (0, 0, 0), (None, 50))
        options_menu.add_element(
            20, Button, 400, 50, "VIDEO", (0, 0, 0), (None, 50))
        options_menu.add_element(
            20, Button, 400, 50, "BACK", (0, 0, 0), (None, 50))
        cls.MENUS["options_menu"] = options_menu

        sound_menu = cls(600, 450, screen_centre, "SOUND",
                         (0, 0, 0), (None, 50), 400, 50)
        sound_menu.add_element(
            0, Slider, SOUND_SETTINGS["effects"], [0, 100], 400, 5, 15,
            "EFFECTS", (0, 0, 0), (None, 30), 200, 40)
        sound_menu.add_element(
            0, Slider, SOUND_SETTINGS["music"], [0, 100], 400, 5, 15,
            "MUSIC", (0, 0, 0), (None, 30), 200, 40)
        sound_menu.add_element(
            20, Button, 400, 50, "LOAD DEFAULT", (0, 0, 0), (None, 50))
        sound_menu.add_element(
            20, Button, 400, 50, "SAVE", (0, 0, 0), (None, 50))
        sound_menu.add_element(
            20, Button, 400, 50, "BACK", (0, 0, 0), (None, 50))
        cls.MENUS["sound_menu"] = sound_menu

        video_menu = cls(600, 485, screen_centre, "VIDEO",
                         (0, 0, 0), (None, 50), 400, 50)
        video_menu.add_element(
            0, Slider, control.gui_settings["resolution"], RESOLUTIONS, 400, 5,
            15, "RESOLUTION", (0, 0, 0), (None, 30), 200, 40)
        video_menu.add_element(
            0, Slider, control.gui_settings["fps"], [1, 60], 400, 5, 15, "FPS",
            (0, 0, 0), (None, 30), 200, 40)
        video_menu.add_element(
            0, Checkbox, control.gui_settings["fullscreen"], 50, 50,
            "FULLSCREEN", (0, 0, 0), (None, 30), 200, 40)
        video_menu.add_element(
            5, Button, 400, 50, "LOAD DEFAULT", (0, 0, 0), (None, 50))
        video_menu.add_element(
            20, Button, 400, 50, "SAVE", (0, 0, 0), (None, 50))
        video_menu.add_element(
            20, Button, 400, 50, "BACK", (0, 0, 0), (None, 50))
        cls.MENUS["video_menu"] = video_menu

        new_game_menu = cls(600, 450, screen_centre, "NEW GAME",
                            (0, 0, 0), (None, 50), 400, 50)
        new_game_menu.add_element(
            20, Button, 400, 50, "EASY", (0, 0, 0), (None, 50))
        new_game_menu.add_element(
            20, Button, 400, 50, "NORMAL", (0, 0, 0), (None, 50))
        new_game_menu.add_element(
            20, Button, 400, 50, "HARD", (0, 0, 0), (None, 50))
        new_game_menu.add_element(
            20, Button, 400, 50, "INSANE", (0, 0, 0), (None, 50))
        new_game_menu.add_element(
            20, Button, 400, 50, "BACK", (0, 0, 0), (None, 50))
        cls.MENUS["new_game_menu"] = new_game_menu

        saves = listdir(r"../Files/Saves/")
        saves = [save for save in saves if save[-4:] == "save"]
        saves = saves[-7:]
        load_game_menu = cls(600, 240 + 70 * len(saves), screen_centre,
                             "LOAD GAME", (0, 0, 0), (None, 50), 400, 50)
        save_game_menu = cls(600, 170 + 70 * len(saves), screen_centre,
                             "SAVE", (0, 0, 0), (None, 50), 400, 50)
        for save in saves:
            load_game_menu.add_element(
                20, Button, 400, 50, save[:-5], (0, 0, 0), (None, 50))
            save_game_menu.add_element(
                20, Button, 400, 50, save[:-5], (0, 0, 0), (None, 50))
        save_game_menu.add_element(
            20, Button, 400, 50, "NEW SAVE", (0, 0, 0), (None, 50))
        load_game_menu.add_element(
            20, Button, 400, 50, "BACK", (0, 0, 0), (None, 50))
        save_game_menu.add_element(
            20, Button, 400, 50, "BACK", (0, 0, 0), (None, 50))
        cls.MENUS["load_game_menu"] = load_game_menu
        cls.MENUS["save_game_menu"] = save_game_menu

        pause_menu = cls(600, 310, screen_centre, "PAUSE",
                         (0, 0, 0), (None, 50), 400, 50)
        pause_menu.add_element(
            20, Button, 400, 50, "RESUME", (0, 0, 0), (None, 50))
        pause_menu.add_element(
            20, Button, 400, 50, "SAVE", (0, 0, 0), (None, 50))
        pause_menu.add_element(
            20, Button, 400, 50, "QUIT", (0, 0, 0), (None, 50))
        cls.MENUS["pause_menu"] = pause_menu

    def draw(self, surface):
        elements = pygame.Surface((self.width, self.height))
        elements.blit(self.image_master, Vector(0, 0))
        for element in self.elements:
            element.draw(elements)
        pygame.draw.polygon(elements, self.frame[0], [
            _ - self.vertices[3] for _ in self.vertices], self.frame[1])
        surface.blit(elements, self.vertices[3])
