import pygame
import pygame_menu

from conf import get_globals

from state_manager import StateManager
state_manager = StateManager()

clock, screen_width, screen_height, surface, menu_theme, font, global_log = get_globals()

CELL_SIZE = 100



class Viewport:
    def __init__(self, width, height):
        self.rect = pygame.Rect(0, 0, width, height)

    def center_on(self, player, grid):
        self.rect.centerx = player.rect.centerx
        self.rect.centery = player.rect.centery

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > grid.width:
            self.rect.right = grid.width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > grid.height:
            self.rect.bottom = grid.height

class Grid:
    def __init__(self, cell_size, num_cells):
        self.cell_size = cell_size
        self.num_cells = num_cells
        self.width = num_cells * cell_size
        self.height = num_cells * cell_size

    def to_pixel(self, grid_x, grid_y):
        return grid_x * self.cell_size, grid_y * self.cell_size
