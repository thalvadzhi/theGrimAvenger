import sys

import pygame
from pygame.math import Vector2 as Vector


# def check_if_groups_collide(first_group, second_group):
#     for first_body in first_group:
#         for second_body in second_group:
#             if first_body.check_if_collide(second_body):
#                 return True
#     return False


class Events:

    def __init__(self):
        self.keyboard_input = []
        self.mouse_input = []
        self.cursor_left_button_is_down = False
        self.cursor_right_button_is_down = False
        self.cursor_location = Vector(0, 0)
        # self.left_button_selectable = []
        # self.right_button_selectable = []
        # self.collisions = []

    def get_user_input(self):
        self.keyboard_input = []
        self.mouse_input = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self.keyboard_input.append(
                    (event.key, Vector(pygame.mouse.get_pos()), True))

            elif event.type == pygame.KEYUP:
                self.keyboard_input.append(
                    (event.key, Vector(pygame.mouse.get_pos()), False))

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.cursor_left_button_is_down = True
                    self.mouse_input.append((1, Vector(event.pos), True))
                elif event.button == 3:
                    self.cursor_right_button_is_down = True
                    self.mouse_input.append((3, Vector(event.pos), True))
                elif event.button == 4 or event.button == 5:
                    self.mouse_input.append((event.button, Vector(event.pos), True))

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.cursor_left_button_is_down = False
                    self.mouse_input.append((1, Vector(event.pos), False))
                elif event.button == 3:
                    self.cursor_right_button_is_down = False
                    self.mouse_input.append((3, Vector(event.pos), False))

        self.cursor_location = Vector(pygame.mouse.get_pos())

#     def check_for_left_button_selectable(self):
#         for selectable in self.left_button_selectable:
#             if selectable.is_point_in_body(self.cursor_location):
#                 return selectable
#         return None
#
#     def check_for_right_button_selectable(self):
#         for selectable in self.right_button_selectable:
#             if selectable.is_point_in_body(self.cursor_location):
#                 return selectable
#         return None
