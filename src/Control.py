from pygame.math import Vector2 as Vector
from Events import Events


def px_to_m(coordinates_px):
    return Vector((coordinates_px[0] * 1, coordinates_px[1] * 1))


class Control(Events):

    def __init__(self, environment):
        Events.__init__(self, environment)
        self.environment = environment
        self.cursor_selected_body = (None, None)

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

    def cursor_controll(self):
        self.cursor_selected_body[0].pull_on_anchor(
            px_to_m(self.cursor_selected_body[1]),
            px_to_m(self.cursor_location_px) - self.cursor_selected_body[1])
        self.cursor_selected_body = (
            self.cursor_selected_body[0], self.cursor_location_px)
