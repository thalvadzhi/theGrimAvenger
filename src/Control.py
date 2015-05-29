import sys
from os import listdir

import pygame
from pickle import load, dump
from pygame.math import Vector2 as Vector

from Player import Player
from Events import Events
from Camera import Camera
from GUI import GUI_SETTINGS, SOUND_SETTINGS, Menu
from Environment import Block, SawBlock, Shadow


class Control(Events):

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
        self.play_music("menu")
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
                self.gui_settings["resolution"])
        self.load_background("loading")
        self.screen.blit(self.background, (0, 0))
        pygame.display.update()

    def init_sound(self):
        self.sound_settings = SOUND_SETTINGS
        self.sound_settings = self.load_settings(r"sound_settings")
        pygame.mixer.music.set_volume(100 / self.sound_settings["music"])

    def init_level(self, level):
        with open(
                r"../Files/Levels/{0}.btmn".format(level), "rb") as level_file:
            self.level = load(level_file)
        self.level_blocks = [Block(*item) for item in self.level["blocks"]]
        self.level_saws = [SawBlock(*item) for item in self.level["sawblocks"]]
        self.level_shadows = [Shadow(*item) for item in self.level["shadows"]]
        self.camera = Camera(self.level["game measures"][0],
                             self.level["game measures"][1],
                             self.gui_settings["resolution"][0],
                             self.gui_settings["resolution"][1])
        self.play_music(self.level["music"])
        # self.current_time = pygame.time.get_ticks()

    def play_music(self, path):
        pygame.mixer.music.load(r"../Files/Sounds/{0}.mp3".format(path))
        pygame.mixer.music.play(-1)

    def load_background(self, path):
        try:
            self.background = pygame.image.load(
                r"../ArtWork/GUI/Backgrounds/{0}.jpg".format(path))
            self.background = pygame.transform.scale(
                self.background, self.gui_settings["resolution"])
        except pygame.error:
            self.background = pygame.Surface(self.gui_settings["resolution"])
            self.background.fill((255, 255, 255))

    def sync_volume(self):
        pygame.mixer.music.set_volume(self.sound_settings["music"] / 100)
        Menu.sync_volume(self)

    def refresh_screen(self):
        if self.take_screenshot:
            self.background.blit(self.screen, (0, 0))
        if self.ingame:
            self.screen.fill((255, 255, 255))
            for needle in self.level_saws:
                needle.draw(self.screen, self.camera)
            for needle in self.level_blocks:
                needle.draw(self.screen, self.camera)
            self.player.display_avatar(self.screen, self.camera)
            for needle in self.level_shadows:
                needle.draw(self.screen, self.camera)
        else:
            if self.current_menu in ["save_game_menu", "pause_menu",
                                     "end_game_menu"]:
                self.take_screenshot = False
            else:
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
            self.sound_settings["effects"] = Menu.MENUS[
                "sound_menu"].elements[1].value
            self.sound_settings["music"] = Menu.MENUS[
                "sound_menu"].elements[2].value
            self.save_settings("sound_settings")
            self.sync_volume()
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
        Menu.MENUS["welcome_menu"].reset_menu_buttons()
        if difficulty is not None:
            self.difficulty = difficulty
            self.init_level("first")
            self.next_step = self.game_handler
            self.player = Player(Vector(self.level["start_position"]))
            self.ingame = True

    def menu_handler(self):
        self.refresh_screen()
        self.get_user_input()
        Menu.MENUS[self.current_menu].handle_input(self)
        getattr(self, self.current_menu + "_control")()

    def game_handler(self):
        for saw in self.level_saws:
            saw.update(self.timer)
        self.get_user_input()
        self.player.handle_input(self)
        self.apply_physics()
        self.refresh_screen()

   # def update_velocity(self, body):
   #     dt_s = self.timer / 1000
   #     # Net resulting force on the puck.
   #     forces_on_body = self.gravity * body.mass + body.impulse / dt_s

   #     # Acceleration from Newton's law.
   #     acceleration = forces_on_body / body.mass

    def apply_physics(self):
        # self.update_velocity(self.player)
        current_time = pygame.time.get_ticks()
        time = current_time - self.last_time 
        self.player.apply_physics(time) 
        collide = [block.rect.check_if_collide(body_part) for block in self.level_blocks
            for body_part in [self.player.body_parts["left_boot"], self.player.body_parts["right_boot"]]]
        if any(_[0] for _ in collide):
            max_MTV = [_[1] for _ in collide if _[0]][0]
            for MTV in collide:
                if MTV[0]:
                    if max_MTV.length() < MTV[1].length():
                        max_MTV = MTV[1]
            self.player.move(max_MTV)
            self.player.velocity[1] = 0
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
