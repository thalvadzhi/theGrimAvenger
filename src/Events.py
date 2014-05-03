import sys
import pygame

from pygame.math import Vector2 as Vector


class Events:

    def __init__(self, envirment):
        # envirment will can hold classes of collision and selectable classes
        # that way one can have events for different envirment like different
        # maps or different menus or windows
        self.envirment = envirment
        self.cursor_left_button_is_down = False
        self.cursor_right_button_is_down = False
        self.cursor_events = []
        self.cursor_location_px = (0, 0)
        self.left_button_selectable = []
        self.right_button_selectable = []
        self.number_inputs = []
        self.letter_inputs = []
        self.special_key_input = []
        self.collisions = []

    def get_user_input(self):
        self.cursor_events = []
        self.number_inputs = []
        self.letter_inputs = []
        self.special_key_input = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.special_key_input.append(pygame.K_ESCAPE)
                elif event.key == pygame.K_1:
                    self.number_inputs.append(1)
                elif event.key == pygame.K_2:
                    self.number_inputs.append(2)
                elif event.key == pygame.K_3:
                    self.number_inputs.append(3)
                elif event.key == pygame.K_4:
                    self.number_inputs.append(4)
                elif event.key == pygame.K_5:
                    self.number_inputs.append(5)
                elif event.key == pygame.K_6:
                    self.number_inputs.append(6)
                elif event.key == pygame.K_7:
                    self.number_inputs.append(7)
                elif event.key == pygame.K_8:
                    self.number_inputs.append(8)
                elif event.key == pygame.K_9:
                    self.number_inputs.append(9)
                elif event.key == pygame.K_0:
                    self.number_inputs.append(0)

                # movement
                elif event.key == pygame.K_a:
                    self.letter_inputs.append(('A', True))
                elif event.key == pygame.K_s:
                    self.letter_inputs.append(('S', True))
                elif event.key == pygame.K_w:
                    self.letter_inputs.append(('W', True))
                elif event.key == pygame.K_d:
                    self.letter_inputs.append(('D', True))

                elif event.key == pygame.K_LEFT:
                    self.special_key_input.append((pygame.K_LEFT, True))
                elif event.key == pygame.K_RIGHT:
                    self.special_key_input.append((pygame.K_RIGHT, True))
                elif event.key == pygame.K_UP:
                    self.special_key_input.append((pygame.K_UP, True))
                elif event.key == pygame.K_DOWN:
                    self.special_key_input.append((pygame.K_DOWN, True))

                # special keys
                elif event.key == pygame.K_SPACE:
                    self.special_key_input.append(pygame.K_SPACE)

                else:
                    pass

            elif event.type == pygame.KEYUP:

                if event.key == pygame.K_a:
                    self.letter_inputs.append(('A', False))
                elif event.key == pygame.K_s:
                    self.letter_inputs.append(('S', False))
                elif event.key == pygame.K_w:
                    self.letter_inputs.append(('W', False))
                elif event.key == pygame.K_d:
                    self.letter_inputs.append(('D', False))

                elif event.key == pygame.K_LEFT:
                    self.special_key_input.append((pygame.K_LEFT, False))
                elif event.key == pygame.K_RIGHT:
                    self.special_key_input.append((pygame.K_RIGHT, False))
                elif event.key == pygame.K_UP:
                    self.special_key_input.append((pygame.K_UP, False))
                elif event.key == pygame.K_DOWN:
                    self.special_key_input.append((pygame.K_DOWN, False))

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.cursor_left_button_is_down = True
                    self.cursor_location_px = event.pos
                    self.cursor_events = (
                        (1, True, self.check_for_left_button_selectable()))
                elif event.button == 2:
                    self.cursor_middle_button_is_down = True
                    self.cursor_events.append((2, True, event.pos))
                elif event.button == 3:
                    self.cursor_right_button_is_down = True
                    self.cursor_location_px = event.pos
                    self.cursor_events = (
                        (3, True, self.check_for_right_button_selectable))
                else:
                    self.cursor_events.append((event.button, True, event.pos))

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.cursor_left_button_is_down = False
                    self.cursor_location_px = event.pos
                    self.cursor_events = (
                        (1, False, self.check_for_right_button_selectable()))
                elif event.button == 2:
                    self.cursor_middle_button_is_down = True
                    self.cursor_events.append((2, False, event.pos))
                elif event.button == 3:
                    self.cursor_right_button_is_down = False
                    self.cursor_location_px = event.pos
                    self.cursor_events = (
                        (3, False, self.check_for_right_button_selectable))
                else:
                    pass

           # elif event.type == pygame.MOUSEMOTION:
           #     self.cursor_events.append((0, event.pos, event.rel))

        # self.cursor_location_px = pygame.mouse.get_pos()

    def check_for_left_button_selectable(self):
        for selectable in self.left_button_selectable:
            if selectable.is_under_cursore(Vector(self.cursor_location_px)):
                return selectable
        return None

    def check_for_right_button_selectable(self):
        for selectable in self.right_button_selectable:
            if selectable.is_under_cursore(Vector(self.cursor_location_px)):
                return selectable
        return None
