import pygame
from enum import Enum

screen_width = 800
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Button:

    def __init__(self, text, button_x, button_y, font, txt_col, colour, func, static_w, static_h,
                 color_per=(74, 72, 70)):
        global screen
        self.text = text
        self.button_x = button_x
        self.button_y = button_y
        self.font = font
        self.txt = font.render(str(text), True, txt_col)
        self.txt_col = txt_col
        self.colour = colour
        self.color_per = color_per
        self.run = func
        x, y, w, h = self.txt.get_rect()
        self.button_w = static_w
        self.button_h = static_h
        self.txt_x = button_x + static_w // 2 - w // 2
        self.txt_y = button_y + static_h // 2 - h // 2

    def draw(self):
        self.txt = self.font.render(str(self.text), True, self.txt_col)
        pygame.draw.rect(screen, self.colour, (self.button_x, self.button_y, self.button_w, self.button_h))
        pygame.draw.rect(screen, self.color_per, (self.button_x, self.button_y, self.button_w, self.button_h), 2)
        screen.blit(self.txt, (self.txt_x, self.txt_y))

