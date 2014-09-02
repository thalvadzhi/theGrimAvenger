from pickle import load, dump
import pygame
from Control import load_settings
from pygame.math import Vector2 as Vector

from BasicShapes import Rectangle
from BasicShapes import Circle

GUI_SETTINGS = {
    "fps": 60,
    "resolution": (1366, 768),
    "fullscreen": False,
}

RESOLUTIONS = [(1280, 1024), (1366, 768), (1600, 1024),
               (1600, 1200), (1920, 1080), (1920, 1200)]


def init():
    # GUI_SETTINGS = load_settings(r"Files/Settings/GUI")
    icon = pygame.image.load(r"../icon.jpg")
    icon = pygame.transform.scale(icon, (32, 32))
    pygame.display.set_icon(icon)
    pygame.display.set_caption("theGrimAvenger", "theGrimAvenger")
    screen = 0
    if GUI_SETTINGS["fullscreen"]:
        screen = pygame.display.set_mode(
            GUI_SETTINGS["resolution"], pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(GUI_SETTINGS["resolution"])
    clock = pygame.time.Clock()
    return screen, clock


class TextBox(Rectangle):

    def __init__(self, width, heigth, position, text, text_colour, text_font,
                 background=None):
        Rectangle.__init__(self, width, heigth, position)
        self.text = text
        self.text_colour = text_colour
        self.text_font = pygame.font.Font(*text_font)
        self.background = background
        self.position = position
        self.create_text_avatar()

    def create_text_avatar(self):
        self.text_avatar = self.text_font.render(
            self.text, 20, self.text_colour)
        if self.text_avatar.get_width() > self.width_m or \
           self.text_avatar.get_height() > self.height_m:
            self.text_avatar = pygame.transform.scale(
                self.text_avatar, (int(self.width_m), int(self.height_m)))

    def draw(self, surface):
        if self.background is not None:
            self.draw(surface, self.background)
        surface.blit(self.text_avatar, self.position - Vector(
            self.text_avatar.get_width(), self.text_avatar.get_height()) / 2)


class Button(Rectangle):

    def __init__(self, action, width, height, position, text, text_colour,
                 text_font, button_type="default"):
        self.action = action
        Rectangle.__init__(self, width, height, position)
        self.states = {}
        for state in ["active", "hover", "normal"]:
            self.load_avatar(
                r"GUI/Button/{0}/{1}.png".format(button_type, state))
            self.scale_avatar(self.width_m, self.height_m)
            self.states[state] = self.imageMaster
        self.state = "normal"
        self.text_box = TextBox(width, height, position, text,
                                text_colour, text_font)
        self.button_type = button_type

    def update_state(self, mouse_position, event):
        mouse_on_button = self.is_point_in_body(mouse_position)
        if self.state is "active":
            if not event:
                if mouse_on_button:
                    self.state = "hover"
                    self.action()
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
        self.imageMaster = self.states[self.state]

    def draw(self, surface):
        self.display_avatar(surface)
        self.text_box.draw(surface)


class Slider(Rectangle):

    def __init__(self, value, values, width, height, puck_radius, position,
                 text, text_colour, text_font, text_box_width, text_box_height,
                 slider_type="default"):
        self.__value = value
        self.values = values
        Rectangle.__init__(self, width, height, position)
        self.puck = Circle(puck_radius, position)
        self.states = {}
        for state in ["active", "hover", "normal"]:
            self.puck.load_avatar(
                r"GUI/Slider/{0}/{1}.png".format(slider_type, state))
            self.puck.scale_avatar(
                self.puck.radius_m * 2, self.puck.radius_m * 2)
            self.states[state] = self.puck.imageMaster
        self.state = "normal"
        self.text_box = TextBox(
            text_box_width, text_box_height, position +
            Vector(0, -self.puck.radius_m - text_box_height / 2), text,
            text_colour, text_font)
        self.slider_type = slider_type

    @property
    def value(self):
        return self.__value

    def update_state(self, mouse_position, event):
        mouse_on_button = self.puck.is_point_in_body(mouse_position)
        if self.state is "active":
            if not event:
                if mouse_on_button:
                    self.state = "hover"
                else:
                    self.state = "normal"
            elif event is None:
                self.move_puck(
                    Vector(mouse_position[0] - self.puck.position_m.x, 0))
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
        self.imageMaster = self.states[self.state]

    def move_puck(self, translation):
        self.puck.move(translation)
        if self.puck.position_m.x < self.position_m.x - self.width_m / 2:
            self.move(Vector(self.position_m.x -
                             self.width_m / 2 - self.puck.position_m.x, 0))
        elif self.puck.position_m.x > self.position_m.x + self.width_m / 2:
            self.move(Vector(self.puck.position_m.x -
                             self.position_m.x - self.width_m / 2, 0))
        if len(self.values) == 2:
            self.__value = self.values[0] + (self.values[1] - self.values[0]) \
                * (self.puck.position_m.x - self.width_m / self.position_m.x +
                   self.width_m / 2)
        else:
            step = round((len(self.values) - 1) *
                         (self.puck.position_m.x - self.width_m /
                          self.position_m.x + self.width_m / 2))
            self.__value = self.values[step]
            self.puck.move(Vector(self.width_m * (step + 1) / len(self.values)
                                  - self.puck.position_m.x, 0))

    def draw(self, surface):
        pygame.draw.polygon(surface, (255, 0, 0), self.vertices)
        self.puck.display_avatar(surface)
        self.text_box.draw(surface)


class Checkbox(Rectangle):

    def __init__(self, value, width, heigth, position, text, text_colour,
                 text_font, text_box_width, text_box_height,
                 checkbox_type="default"):
        self.__value = value
        Rectangle.__init__(self, width, heigth, position)
        self.states = {}
        for state in ["checked", "unchecked",
                      "checked_hover", "unchecked_hover"]:
            self.load_avatar(
                r"GUI/Checkbox/{0}/{1}.png".format(checkbox_type, state))
            self.scale_avatar(self.width_m, self.height_m)
            self.states[state] = self.imageMaster
        self.state = "unchecked"
        self.text_box = TextBox(
            text_box_width, text_box_height, position +
            Vector((self.width_m + text_box_width) / 2, 0),
            text, text_colour, text_font)
        self.checkbox_type = checkbox_type

    @property
    def value(self):
        return self.__value

    def update_state(self, mouse_position, event):
        mouse_on_button = self.is_point_in_body(mouse_position)
        if event:
            if mouse_on_button:
                if self.state is "checked_hover" or self.state is "checked":
                    self.__value = False
                    self.state = "unchecked_hover"
                else:
                    self.__value = True
                    self.state = "checked_hover"
        elif event is None:
            if mouse_on_button:
                if self.state is "checked":
                    self.state = "checked_hover"
                elif self.state is "unchecked":
                    self.state = "unchecked_hover"
            else:
                if self.state is "checked_hover":
                    self.state = "checked"
                elif self.state is "unchecked_hover":
                    self.state = "unchecked"
        self.imageMaster = self.states[self.state]

    def draw(self, surface):
        self.display_avatar(surface)
        self.text_box.draw(surface)


class Menu(Rectangle):

    COMPONENTS = {"Button": Button, "Slider": Slider, "Checkbox": Checkbox}

    def __init__(self, width, heigth, position, title, title_colour,
                 title_font, title_box_width, title_box_height,
                 background="default"):
        Rectangle.__init__(self, width, heigth, position)
        self.elements = []
        self.load_avatar(r"GUI/Menu/{0}.jpg".format(background))
        self.text_box = TextBox(
            title_box_width, title_box_height,
            Vector(width / 2, title_box_height / 2),
            title, title_colour, title_font)

    def add_element(self, element_type, value):
        pass
       #self.elements.append(Menu.COMPONENTS[element_type]

    def handle_input(self, control):
        for event in control.mouse_input:
            if event[0] == 1:
                for element in self.elements:
                    element.update_state(event[1] - self.vertices[3], event[2])
        for event in control.keyboard_input:
            if event[2] and event[0] in set(range(48, 59)) and \
                    event[0] <= len(self.elements) and \
                    isinstance(self.elements[event[0] - 1], Button):
                self.elements[event[0] - 1].action()
        for element in self.elements:
            element.update_state(
                control.cursor_location - self.vertices[3], None)  

    def draw(self, surface):
        elements = pygame.Surface((self.width_m, self.height_m))
        elements.blit(self.imageMaster, Vector(0, 0))
        for element in self.elements:
            element.draw(elements)
        self.text_box.draw(elements)
        surface.blit(elements, self.vertices[3])
