import sys
import pygame

from pygame.math import Vector2 as Vector


class Events:

    def __init__(self, envirment):
        # envirment will can hold classes of collision and selectable classes
        # that way one can have events for different envirment like different
        # maps or different menus or windows
        self.envirment = envirment
        self.current_event = None
        self.cursor_left_button_is_down = False
        self.cursor_right_button_is_down = False
        self.cursor_location_px = Vector(0, 0)
        self.left_button_selectable = []
        self.right_button_selectable = []
        self.collisions = []

    def get_user_input(self):
        self.current_event = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pass

                elif event.key == pygame.K_1:
                    self.current_event = 1
                elif event.key == pygame.K_2:
                    self.current_event = 2
                elif event.key == pygame.K_3:
                    self.current_event = 3
                elif event.key == pygame.K_4:
                    self.current_event = 4
                elif event.key == pygame.K_5:
                    self.current_event = 5
                elif event.key == pygame.K_6:
                    self.current_event = 6
                elif event.key == pygame.K_7:
                    self.current_event = 7
                elif event.key == pygame.K_8:
                    self.current_event = 8
                elif event.key == pygame.K_9:
                    self.current_event = 9
                elif event.key == pygame.K_0:
                    self.current_event = 0

                # movement
                elif event.key == pygame.K_a:
                    self.current_event = ('A', True)
                elif event.key == pygame.K_s:
                    self.current_event = ('S', True)
                elif event.key == pygame.K_w:
                    self.current_event = ('W', True)
                elif event.key == pygame.K_d:
                    self.current_event = ('D', True)

                elif event.key == pygame.K_LEFT:
                    self.current_event = ('A', True)
                elif event.key == pygame.K_RIGHT:
                    self.current_event = ('D', True)
                elif event.key == pygame.K_UP:
                    self.current_event = ('W', True)
                elif event.key == pygame.K_DOWN:
                    self.current_event = ('S', True)

                # special keys
                elif event.key == pygame.K_SPACE:
                    self.current_event = ' '

                else:
                    pass

            elif event.type == pygame.KEYUP:

                 # movement
                if event.key == pygame.K_a:
                    self.current_event = ('A', True)
                elif event.key == pygame.K_s:
                    self.current_event = ('S', True)
                elif event.key == pygame.K_w:
                    self.current_event = ('W', True)
                elif event.key == pygame.K_d:
                    self.current_event = ('D', True)

                elif event.key == pygame.K_LEFT:
                    self.current_event = ('A', True)
                elif event.key == pygame.K_RIGHT:
                    self.current_event = ('D', True)
                elif event.key == pygame.K_UP:
                    self.current_event = ('W', True)
                elif event.key == pygame.K_DOWN:
                    self.current_event = ('S', True)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.cursor_left_button_is_down = True
                    self.cursor_location_px = Vector(event.pos)
                    self.current_event = (
                        1, True, self.check_for_left_button_selectable(),
                        Vector(event.pos))
               # elif event.button == 2:
               #     self.cursor_middle_button_is_down = True
               #     self.cursor_events.append((2, True, event.pos))
                elif event.button == 3:
                    self.cursor_right_button_is_down = True
                    self.cursor_location_px = Vector(event.pos)
                    self.current_event = (
                        3, True, self.check_for_right_button_selectable())
                else:
                    pass
                  # self.cursor_events.append((event.button, True, event.pos))

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.cursor_left_button_is_down = False
                    self.cursor_location_px = Vector(event.pos)
                    self.current_event = (
                        1, False, self.check_for_left_button_selectable())
              #  elif event.button == 2:
              #      self.cursor_middle_button_is_down = True
              #      self.cursor_events.append((2, False, event.pos))
                elif event.button == 3:
                    self.cursor_right_button_is_down = False
                    self.cursor_location_px = Vector(event.pos)
                    self.current_event = (
                        3, False, self.check_for_right_button_selectable())
                else:
                    pass

           # elif event.type == pygame.MOUSEMOTION:
           #     self.cursor_events.append((0, event.pos, event.rel))

        self.cursor_location_px = Vector(pygame.mouse.get_pos())

    def check_for_left_button_selectable(self):
        for selectable in self.left_button_selectable:
            if selectable.is_under_cursor(self.cursor_location_px):
                return selectable
        return None

    def check_for_right_button_selectable(self):
        for selectable in self.right_button_selectable:
            if selectable.is_under_cursor(self.cursor_location_px):
                return selectable
        return None
