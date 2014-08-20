"""Everything which visualises should be here or iported here
"""  # make it meaningfull

import pygame

from pygame.color import THECOLORS


class Slider:

    def __init__(self, start, end):
        self.start = start
        self.end = end

class GameWindow:
    
    """
    """

    def __init__(self, width_px, heigth_px, title, icon_path):
        """
        """

        self.title = title
        #pygame.display.set_caption(title, get_image_file(icon_path))

        self.icon_path = icon_path
        # pygame.display.set_icon(get_image_file(icon_path))

        # surface should be created after setting the window icon
        # or set_icon might not work
        self.width_px = width_px
        self.heigth_px = heigth_px
        self.surface = pygame.display.set_mode((width_px, heigth_px))
