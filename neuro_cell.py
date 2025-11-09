#Cell class
import pygame
from neuro_defaults import *

class Cell:

    number_surfaces = []*8
    sketch_surfaces = []*8

    def __init__(self, value, row, col, screen):
        self.value = value
        self.sketched_value = 0
        self.permanent = (value != 0)
        self.locked = (value != 0)
        self.screen_x, self.screen_y = ((FRAME_SIZE[0] / 8) * (col + 1) - ((FRAME_SIZE[0] / 8)) / 2), ((FRAME_SIZE[1] / 8) * (row + 1) - ((FRAME_SIZE[1] / 8)) / 2)

        self.rect = self.number_surfaces[value - 1].get_rect(
            center = (self.screen_x, self.screen_y)
        )

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value
        self.rect = self.sketch_surfaces[self.sketched_value - 1].get_rect(
            bottomright = (self.screen_x, self.screen_y)
        )

    def confirm(self):
        self.value = self.sketched_value
        if self.value != 0:
            self.locked = True
            self.rect = self.number_surfaces[self.value - 1].get_rect(
                center = (self.screen_x, self.screen_y)
            )

    def draw(self, screen):
        if self.value > 0:
            screen.blit(self.number_surfaces[self.value - 1], self.rect)
        else:
            if self.sketched_value > 0:
                screen.blit(self.sketch_surfaces[self.sketched_value - 1], self.rect)
