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


