import unittest
from button import Button
import pygame
pygame.init()


class ButtonTest(unittest.TestCase):
    def test_button(self):
        button = Button((0, 0), (50, 50), "TEST", (0, 0, 0), (0, 0, 0))

        class EVT:
            def __init__(self, event, key):
                self.type = event
                self.key = key
        self.assertEqual(button.is_pressed((10, 10), [EVT(6, 0)]), True)
        self.assertEqual(button.is_pressed((400, 10), [EVT(6, 0)]), False)

    def test_drawing(self):
        screen = pygame.display.set_mode((0, 0))
        button = Button((0, 0), (50, 50), "TEST", (0, 0, 0), (0, 0, 0))
        button.draw(screen)

if __name__ == '__main__':
    unittest.main()
