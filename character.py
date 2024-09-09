from boat import Boat
from garage import Garage
from battle import get_level_from_experience
from dataclasses import dataclass, field


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


# class Character:
#     def __init__(self, character_data, character_id):
#         if isinstance(character_data, dict):
#             self.character_id = character_id
#             self.name = character_data.get("name", "")
#             self.fishing_experience = character_data.get("fishing_experience", 0)
#             self.age = get_level_from_experience(self.fishing_experience)
#             self.strength = character_data.get("strength", 1)
#             self.stamina = character_data.get("stamina", 100)
#             self.max_stamina = character_data.get("max_stamina", 100)
#             self.gear = character_data.get("gear", {})
#             boats = character_data.get("boats", [])
#             self.garage = Garage(boats)
#             self.boats = [boat for boat in self.garage.boats]
#         else:
#             self.character_id = character_id
#             self.name = character_data.name
#             self.fishing_experience = character_data.fishing_experience
#             self.age = get_level_from_experience(self.fishing_experience)
#             self.strength = character_data.strength
#             self.max_stamina = character_data.max_stamina
#             self.stamina = character_data.stamina
#             self.gear = character_data.gear
#             boats = character_data.boats
#             self.garage = Garage(boats)
#             self.boats = [boat for boat in self.garage.boats]
