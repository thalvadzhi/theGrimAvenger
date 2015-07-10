import sys
import json
from copy import copy
from os import listdir

import pygame
from pickle import load, dump
from pygame.math import Vector2 as Vector

from Serialize import Decoder
from Light import Light
from Player import Player
from events import Events
from Camera import Camera
from gui import GUI_SETTINGS, SOUND_SETTINGS, Menu, SoundEffect
from Environment import Block, SawBlock


class Control(Events):

    BACKGROUNDS = {}

    def __init__(self):
        Events.__init__(self)
        self.gravity = Vector(0.0, 0.1)
        self.init_graphics()
        self.init_sound()
        Menu.init_menus(self)
        self.current_menu = "welcome_menu"
        self.camera = 0
        self.clock = pygame.time.Clock()
        self.time = pygame.time
        self.last_time = 0
        self.take_screenshot = False
        self.ingame = False
        SoundEffect.play_music("menu.mp3")
        self.next_step = self.menu_handler
        self.load_background("welcome")

#     def handle_user_input(self):
#         self.get_user_input()
#         if isinstance(self.current_event, int):
#             pass
#         elif isinstance(self.current_event, str):
#             pass
#         elif isinstance(self.current_event, tuple):
#             if self.current_event[0] is str:
#                 pass
#             elif isinstance(self.current_event[0], int):
#                 if self.current_event[0] == 3:
#                     pass
#                 elif self.current_event[0] == 1:
#                     if self.current_event[1]:
#                         self.cursor_selected_body = (
#                             self.current_event[2], self.current_event[3])
#                     else:
#                         self.cursor_selected_body = (None, None)
#
#         if self.cursor_selected_body[0] is not None:
#             self.cursor_controll()

    def init_graphics(self):
        self.gui_settings = GUI_SETTINGS
        self.gui_settings = self.load_settings(r"gui_settings")
        icon = pygame.image.load(r"../icon.jpg")
        icon = pygame.transform.scale(icon, (32, 32))
        pygame.display.set_icon(icon)
        pygame.display.set_caption("theGrimAvenger", "theGrimAvenger")
        if self.gui_settings["fullscreen"]:
            self.screen = pygame.display.set_mode(
                self.gui_settings["resolution"], pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(
                self.gui_settings["resolution"], pygame.HWSURFACE)
        self.load_background("loading")
        self.screen.blit(self.background, (0, 0))
        pygame.display.update()

    def init_sound(self):
        global SOUND_SETTINGS
        self.sound_settings = SOUND_SETTINGS
        self.sound_settings = self.load_settings("sound_settings")
        SOUND_SETTINGS["effects"] = self.sound_settings["effects"]
        SOUND_SETTINGS["music"] = self.sound_settings["music"]
        SoundEffect.set_music_volume(SOUND_SETTINGS["music"])
        delattr(self, "sound_settings")

    def init_level(self, level):
        world = ""
        with open(
                r"../Files/Levels/{0}.btmn".format(level), "r") as level_file:
            world = level_file.readline()
            self.lights = level_file.readline()
            self.level_settings = level_file.readline()
            self.swinging_lights = level_file.readline()

        self.level_settings = json.loads(self.level_settings, cls=Decoder)
        Light.set_up_surfaces(self.level_settings.width,
                              self.level_settings.height)
        self.swinging_lights = json.loads(self.swinging_lights, cls=Decoder)

        world = json.loads(world, cls=Decoder)
        self.lights = json.loads(self.lights, cls=Decoder)

        self.level_blocks = list(
            filter(
                lambda item: isinstance(
                    item,
                    Block),
                world))
        self.level_saws = list(
            filter(
                lambda item: isinstance(
                    item,
                    SawBlock),
                world))

        for light in self.lights + self.swinging_lights:
            light.update_obstacles(self.level_blocks)

        self.camera = Camera(self.level_settings.width,
                             self.level_settings.height,
                             self.gui_settings["resolution"][0],
                             self.gui_settings["resolution"][1])
        SoundEffect.play_music(r"{0}.mp3".format(self.level_settings.music))
        self.player = Player(Vector(self.level_settings.start_position), self)
        self.player.equipment.equip("Batarang", 3)
        # self.current_time = pygame.time.get_ticks()

    def load_background(self, path):
        if path in Control.BACKGROUNDS:
            self.background = Control.BACKGROUNDS[path]
            return
        try:
            self.background = pygame.image.load(
                r"../ArtWork/GUI/Backgrounds/{0}.jpg".format(path))
            self.background = pygame.transform.scale(
                self.background, self.gui_settings["resolution"])
        except pygame.error:
            self.background = pygame.Surface(self.gui_settings["resolution"])
            self.background.fill((255, 255, 255))
        Control.BACKGROUNDS[path] = copy(self.background)

    def refresh_screen(self):
        if self.ingame or self.take_screenshot:
            self.screen.fill((255, 255, 255))
            Light.nullify_shadow()
            Light.nullify_light()

            for light in self.lights:
                light.draw_shadow(self.camera)
                light.draw_light(self.camera)
            for swinging_light in self.swinging_lights:
                swinging_light.draw(self.screen, self.camera)
            Light.draw_everything(self.screen)

            for saw in self.level_saws:
                saw.draw(self.screen, self.camera)
            for block in self.level_blocks:
                block.draw(self.screen, self.camera)

            self.player.display_avatar(self.screen, self.camera)
            self.player.equipment.draw(self.screen, self.camera)
        if not self.ingame:
            if self.take_screenshot:
                self.background.blit(self.screen, (0, 0))
                self.take_screenshot = False

            self.screen.blit(self.background, (0, 0))
            Menu.MENUS[self.current_menu].draw(self.screen)
        pygame.display.update()

    def welcome_menu_control(self):
        if Menu.MENUS["welcome_menu"].elements[1].clicked:
            self.current_menu = "new_game_menu"
        elif Menu.MENUS["welcome_menu"].elements[2].clicked:
            self.current_menu = "options_menu"
        elif Menu.MENUS["welcome_menu"].elements[3].clicked:
            self.current_menu = "options_menu"
        elif Menu.MENUS["welcome_menu"].elements[4].clicked:
            sys.exit()
        Menu.MENUS["welcome_menu"].reset_menu_buttons()

    def options_menu_control(self):
        if Menu.MENUS["options_menu"].elements[1].clicked:
            self.current_menu = "sound_menu"
        elif Menu.MENUS["options_menu"].elements[2].clicked:
            self.current_menu = "video_menu"
        elif Menu.MENUS["options_menu"].elements[3].clicked:
            self.current_menu = "welcome_menu"
        Menu.MENUS["options_menu"].reset_menu_buttons()

    def sound_menu_control(self):
        if Menu.MENUS["sound_menu"].elements[3].clicked:
            Menu.MENUS[
                "sound_menu"].elements[1].value = SOUND_SETTINGS["effects"]
            Menu.MENUS[
                "sound_menu"].elements[2].value = SOUND_SETTINGS["music"]
        elif Menu.MENUS["sound_menu"].elements[4].clicked:
            SOUND_SETTINGS["effects"] = Menu.MENUS[
                "sound_menu"].elements[1].value
            SoundEffect.set_music_volume(Menu.MENUS[
                "sound_menu"].elements[2].value)
            self.sound_settings = SOUND_SETTINGS
            self.save_settings("sound_settings")
            delattr(self, "sound_settings")
        elif Menu.MENUS["sound_menu"].elements[5].clicked:
            self.current_menu = "options_menu"
        Menu.MENUS["sound_menu"].reset_menu_buttons()

    def video_menu_control(self):
        if Menu.MENUS["video_menu"].elements[4].clicked:
            Menu.MENUS[
                "video_menu"].elements[1].value = GUI_SETTINGS["resolution"]
            Menu.MENUS[
                "video_menu"].elements[2].value = GUI_SETTINGS["fps"]
            Menu.MENUS[
                "video_menu"].elements[3].value = GUI_SETTINGS["fullscreen"]
        elif Menu.MENUS["video_menu"].elements[5].clicked:
            self.gui_settings["resolution"] = Menu.MENUS[
                "video_menu"].elements[1].value
            self.gui_settings["fps"] = Menu.MENUS[
                "video_menu"].elements[2].value
            self.gui_settings["fullscreen"] = Menu.MENUS[
                "video_menu"].elements[3].value
            self.save_settings("gui_settings")
        elif Menu.MENUS["video_menu"].elements[6].clicked:
            self.current_menu = "options_menu"
        Menu.MENUS["video_menu"].reset_menu_buttons()

    def new_game_menu_control(self):
        difficulty = None
        if Menu.MENUS["new_game_menu"].elements[1].clicked:
            difficulty = "easy"
        elif Menu.MENUS["new_game_menu"].elements[2].clicked:
            difficulty = "normal"
        elif Menu.MENUS["new_game_menu"].elements[3].clicked:
            difficulty = "hard"
        elif Menu.MENUS["new_game_menu"].elements[4].clicked:
            difficulty = "insane"
        elif Menu.MENUS["new_game_menu"].elements[5].clicked:
            self.current_menu = "welcome_menu"
        Menu.MENUS["new_game_menu"].reset_menu_buttons()
        if difficulty is not None:
            self.difficulty = difficulty
            self.init_level("level2")
            self.next_step = self.game_handler
            self.ingame = True

    def game_over_menu_control(self):
        if Menu.MENUS["game_over_menu"].elements[1].clicked:
            self.player = Player(
                Vector(
                    self.level_settings.start_position),
                self)
            self.next_step = self.game_handler
            self.ingame = True
        elif Menu.MENUS["game_over_menu"].elements[2].clicked:
            self.load_background("welcome")
            self.current_menu = "welcome_menu"
        Menu.MENUS["game_over_menu"].reset_menu_buttons()

    def menu_handler(self):
        self.get_user_input()
        Menu.MENUS[self.current_menu].handle_input(self)
        getattr(self, self.current_menu + "_control")()
        self.refresh_screen()

    def game_handler(self):
        for swinging_light in self.swinging_lights:
            swinging_light.update()
        self.get_user_input()
        self.player.handle_input()
        self.apply_physics()
        for saw in self.level_saws:
            saw.update(self.timer)
            if self.player.check_if_collide(saw.collision_circle):
                self.take_screenshot = True
                self.next_step = self.menu_handler
                self.current_menu = "game_over_menu"
                self.ingame = False
        self.player.equipment.update()
        self.refresh_screen()

#    def update_velocity(self, body):
#        dt_s = self.timer / 1000
#    Net resulting force on the puck.
#        forces_on_body = self.gravity * body.mass + body.impulse / dt_s

#    Acceleration from Newton's law.
#        acceleration = forces_on_body / body.mass

    def apply_physics(self):
        # self.update_velocity(self.player)
        current_time = pygame.time.get_ticks()
        time = current_time - self.last_time
        self.player.apply_physics(time, self)
        self.last_time = current_time

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

    def save_settings(self, path):
        with open(r"../Files/Settings/{0}".format(path),
                  'wb') as settings_file:
            dump(getattr(self, path), settings_file)
