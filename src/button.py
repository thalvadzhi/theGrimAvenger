from pygame import MOUSEBUTTONUP, font
from pygame.math import Vector2 as Vector
from basicshapes import Rectangle


class Button:
    def __init__(self, position, size, message, colour, text_colour):
        self.rect = Rectangle(size[0], size[1],
                              Vector(position[0] + size[0] // 2,
                                     position[1] + size[1] // 2))
        self.message = message
        self.colour = colour
        self.text_colour = text_colour
        self.font = font.Font(None, 32)
        self.position = position

    def is_pressed(self, mouse_position, events):
        for event in events:
            if event.type == MOUSEBUTTONUP:
                if self.rect.is_point_in_body(mouse_position):
                    return True
        return False

    def draw(self, screen):
        self.rect.draw(screen, self.colour)
        text = self.font.render(self.message, 20, self.text_colour)
        screen.blit(text, self.position)
