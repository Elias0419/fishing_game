from dataclasses import dataclass, field
from battle import Battle
import random


def calculate_fish_weight(length_inch):
    a = random.uniform(0.00023, 0.0003)
    b = 3
    weight_lbs = a * (length_inch**b)
    return weight_lbs


@dataclass
class Fish:
    name: str = "Generic Fish"
    stamina: int = 100
    # length_inch: float = None
    # weight_lbs: float = None # TEST
    minimum_fishing_experience: int = 0
    gives_exp: int = 0
    eats: list[str] = field(default_factory=lambda: ["all"])
    generic_type: str = "fish"
    specific_type: str = "generic_fish"
    subtype: str = "generic_fish_subtype"

    length_inch: float = 6 # Remove me
    weight_lbs: float = 11 # Remove me

    # def __post_init__(self): # TEST
    #     if self.length_inch is None:
    #         self.length_inch = random.uniform(1, 10)
    #     self.weight_lbs = calculate_fish_weight(self.length_inch)


@dataclass
class Goldfish(Fish):
    name: str = "Goldfish"
    stamina: int = 10
    eats: list[str] = field(default_factory=lambda: ["Worm", "Small Bug"])
    specific_type: str = "goldfish"
    subtype: str = "bony_fishes"



    minimum_fishing_experience: int = 11  # TEST

    # def __post_init__(self): # TEST
    #     self.length_inch = random.uniform(1, 10)
    #     self.gives_exp: int = random.randint(3, 10)
    #     super().__post_init__()


@dataclass
class Bluegill(Fish):
    name: str = "Bluegill"
    stamina: int = 20
    # length_inch: float = random.uniform(3, 12)

    eats: list[str] = field(default_factory=lambda: ["Worm", "Small Bug"])
    specific_type: str = "bluegill"
    subtype: str = "bony_fishes"

    minimum_fishing_experience: int = 20

    def __post_init__(self):
        self.gives_exp: int = random.randint(5, 15)
        self.length_inch = random.uniform(3, 12)
        super().__post_init__()


@dataclass
class Catfish(Fish):
    name: str = "Catfish"
    stamina: int = 50
    # length_inch: float = random.uniform(12, 24)

    eats: list[str] = field(default_factory=lambda: ["Worm", "Cut Bait"])
    specific_type: str = "catfish"
    subtype: str = "bony_fishes"

    minimum_fishing_experience: int = 100

    def __post_init__(self):
        self.gives_exp: int = random.randint(10, 20)
        self.length_inch = random.uniform(12, 24)
        super().__post_init__()


@dataclass
class Carp(Fish):
    name: str = "Carp"
    stamina: int = 30
    # length_inch: float = random.uniform(12, 36)

    eats: list[str] = field(default_factory=lambda: ["Worm", "Corn", "Dough Bait"])
    specific_type: str = "carp"
    subtype: str = "bony_fishes"

    minimum_fishing_experience: int = 250

    def __post_init__(self):
        self.gives_exp: int = random.randint(15, 25)
        self.length_inch = random.uniform(12, 36)
        super().__post_init__()


@dataclass
class Sunfish(Fish):
    name: str = "Sunfish"
    stamina: int = 15
    # length_inch: float = random.uniform(3, 10)
    minimum_fishing_experience: int = 500
    eats: list[str] = field(default_factory=lambda: ["Worm", "Bread"])
    specific_type: str = "sunfish"
    subtype: str = "bony_fishes"

    def __post_init__(self):
        self.gives_exp: int = random.randint(3, 10)
        self.length_inch = random.uniform(3, 10)
        super().__post_init__()


################################################
@dataclass
class Trout(Fish):
    name: str = "Trout"
    stamina: int = random.randint(30, 50)
    eats: list[str] = field(default_factory=lambda: ["Insects", "Small Fish"])

    specific_type: str = "trout"
    subtype: str = "bony_fishes"

    def __post_init__(self):
        self.gives_exp: int = random.randint(10, 20)
        self.length_inch = random.uniform(12, 30)
        super().__post_init__()


@dataclass
class Salmon(Fish):
    name: str = "Salmon"
    stamina: int = random.randint(50, 70)
    # length_inch: float = random.uniform(20, 36)
    eats: list[str] = field(default_factory=lambda: ["Small Fish", "Insects"])

    specific_type: str = "salmon"
    subtype: str = "bony_fishes"

    def __post_init__(self):
        self.gives_exp: int = random.randint(20, 30)
        self.length_inch = random.uniform(20, 36)
        super().__post_init__()


@dataclass
class Sturgeon(Fish):
    name: str = "Sturgeon"
    stamina: int = random.randint(60, 80)
    # length_inch: float = random.uniform(48, 72)
    eats: list[str] = field(
        default_factory=lambda: ["Shellfish", "Worm", "Small Fish", "Medium Fish"]
    )

    specific_type: str = "sturgeon"
    subtype: str = "bony_fishes"

    def __post_init__(self):
        self.gives_exp: int = random.randint(25, 35)
        self.length_inch = random.uniform(48, 72)
        super().__post_init__()


@dataclass
class Minnow(Fish):
    name: str = "Minnow"
    stamina: int = random.randint(5, 15)
    # length_inch: float = random.uniform(1, 3)
    eats: list[str] = field(default_factory=lambda: ["Small Insects"])

    specific_type: str = "minnow"
    subtype: str = "bony_fishes"

    def __post_init__(self):
        self.gives_exp: int = random.randint(1, 5)
        self.length_inch = random.uniform(1, 3)
        super().__post_init__()


@dataclass
class GreatWhite(Fish):
    name: str = "Great White Shark"
    minimum_fishing_experience: int = 100
    specific_type: str = "great_white"
    subtype: str = "sharks"
