from dataclasses import dataclass, field
from random import choices

# from fish import *
import importlib


@dataclass
class Location:
    name: str = "Generic Location"
    minimum_level: int = 0
    water_type: str = "fresh"
    water_movement: str = "flat"
    wind: str = "still"
    fish_probability: dict[str, float] = field(default_factory=lambda: {"any": 1})

    def get_fish(self):
        fish_types = list(self.fish_probability.keys())
        probabilities = list(self.fish_probability.values())
        fish_class_name = choices(fish_types, weights=probabilities, k=1)[0]
        fish_module = importlib.import_module("fish")
        fish_class = getattr(fish_module, fish_class_name)
        return fish_class()


@dataclass
class NeighborhoodPond(Location):
    name: str = "Neighborhood Pond"
    fish_probability: dict[str, float] = field(
        default_factory=lambda: {
            "Goldfish": 1,
            # "Goldfish": 0.5, # TEST
            # "Bluegill": 0.3,
            # "Catfish": 0.1,
            # "Carp": 0.05,
            # "Sunfish": 0.05
        }
    )


@dataclass
class StreamInTheWoods(Location):
    name: str = "Stream in the Woods"
    water_movement: str = "flowing"
    wind: str = "light_breeze"
    fish_probability: dict[str, float] = field(
        default_factory=lambda: {
            "Trout": 0.4,
            "Salmon": 0.15,
            "Sturgeon": 0.1,
            "Minnow": 0.05,
        }
    )
