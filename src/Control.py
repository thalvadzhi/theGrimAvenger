from os import listdir

import pygame
from pickle import load, dump
from Vec2D import Vec2d as Vector

from Events import Events
from Camera import Camera
from GUI import GUI_SETTINGS, SOUND_SETTINGS, Menu
from Environment import Block, SawBlock, Shadow


class Control(Events):

    def __init__(self):
        Events.__init__(self)
        self.init_graphics()
        self.init_sound()
        Menu.init_menus(self)
        self.camera = 0
#        self.current_menu =
        self.clock = pygame.time.Clock()

    def handle_user_input(self):
        self.get_user_input()
        if isinstance(self.current_event, int):
            pass
        elif isinstance(self.current_event, str):
            pass
        elif isinstance(self.current_event, tuple):
            if self.current_event[0] is str:
                pass
            elif isinstance(self.current_event[0], int):
                if self.current_event[0] == 3:
                    pass
                elif self.current_event[0] == 1:
                    if self.current_event[1]:
                        self.cursor_selected_body = (
                            self.current_event[2], self.current_event[3])
                    else:
                        self.cursor_selected_body = (None, None)

        if self.cursor_selected_body[0] is not None:
            self.cursor_controll()

    def init_graphics(self):
        self.gui_settings = GUI_SETTINGS
        self.gui_settings = self.load_settings(r"gui_settings")
        icon = pygame.image.load(r"../icon.jpg")
        icon = pygame.transform.scale(icon, (32, 32))
        pygame.display.set_icon(icon)
        pygame.display.set_caption("theGrimAvenger", "theGrimAvenger")
        if GUI_SETTINGS["fullscreen"]:
            self.screen = pygame.display.set_mode(
                GUI_SETTINGS["resolution"], pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(GUI_SETTINGS["resolution"])

    def init_sound(self):
        self.sound_settings = SOUND_SETTINGS
        self.sound_settings = self.load_settings(r"sound_settings")
        pygame.mixer.music.set_volume(100 / self.sound_settings["music"])

    def init_level(self, level):
        self.level = self.load_settings(r"../Files/Levels/{0}".format(level))
        self.world = self.level["world"]
        for item in self.world:
            item.load_texture()
        self.camera = Camera(self.level["game measures"][0],
                             self.level["game measures"][1],
                             self.gui_settings["resolution"][0],
                             self.gui_settings["resolution"][1])
        Shadow.set_up(self.level["game measures"][0],
                      self.level["game measures"][1])

    def sync_volume(self):
        Menu.sync_volume(self)

    def refresh_screen(self):
        self.screen.fill((0, 0, 0))
        self.background.draw(self.screen)
        pygame.display.update()

    def menu_loop(self):
        pass

    def game_loop(self):
        while self.in_game:
            self.refresh_screen()
            self.clock.tick(self.gui_settings["fps"])

#    def cursor_controll(self):
#        self.cursor_selected_body[0].pull_on_anchor(
#            self.cursor_selected_body[1],
#            self.cursor_location_px - self.cursor_selected_body[1])
#        self.cursor_selected_body = (
#            self.cursor_selected_body[0], self.cursor_location_px)

    def load_settings(self, path):
        if path not in listdir(r"../Files/Settings/"):
            return getattr(self, path)
        with open(r"../Files/Settings/{0}".format(path),
                  "rb") as settings_file:
            return load(settings_file)

    def save_settings(self, path, settings):
        with open(r"../Files/Settings/{0}".format(path),
                  'wb') as settings_file:
            dump(settings, settings_file)
