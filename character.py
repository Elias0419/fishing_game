from boat import Boat
from garage import Garage
from util import get_level_from_experience
from dataclasses import dataclass, field
import pygame

@dataclass
class Character:
    character_id: int
    name: str = "Dummy"
    fishing_experience: int = 0
    age: int = field(init=False)
    strength: int = 1
    stamina: int = 100
    max_stamina: int = 100
    gear: dict = field(default_factory=dict)
    boats: list = field(default_factory=list)
    garage: "Garage" = field(init=False)

    def __post_init__(self):
        self.age = get_level_from_experience(self.fishing_experience)
        self.garage = Garage(self.boats)
        self.boats = [boat for boat in self.garage.boats]


class Player(pygame.sprite.Sprite):
    def __init__(self, character, grid, initial_position):
        super().__init__()
        self.character = character
        self.grid = grid
        self.position = initial_position

        # Dummy sprite for development REMOVE ME
        self.size = 30
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill((255, 0, 0))
        # self.rect = self.image.get_rect(topleft=self.grid.to_pixel(*position))
        self.rect = pygame.Rect(grid.to_pixel(*initial_position), (self.size, self.size))

    def move(self, dx, dy):
        new_position = (self.position[0] + dx, self.position[1] + dy)
        if 0 <= new_position[0] < self.grid.width and 0 <= new_position[1] < self.grid.height:
            self.position = new_position
            self.rect.topleft = self.grid.to_pixel(*self.position)

    def update(self, keys_pressed):
        dx, dy = 0, 0
        if keys_pressed[pygame.K_w]:
            dy -= 1
        if keys_pressed[pygame.K_s]:
            dy += 1
        if keys_pressed[pygame.K_a]:
            dx -= 1
        if keys_pressed[pygame.K_d]:
            dx += 1
        self.move(dx, dy)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
