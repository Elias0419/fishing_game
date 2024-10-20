from dataclasses import dataclass, field, fields
from collections import namedtuple
import pickle


@dataclass
class BattleState:
    drag_too_high_count: int = None
    drag_too_low_count: int = None
    max_safe_drag: int = None
    first_round: bool = None


@dataclass
class LocationState:
    name: str = None
    unlocked: bool = False
    fish_probability: dict[str, float] = field(default_factory=dict)


@dataclass
class WorldState:
    locations: list[LocationState] = field(default_factory=list)


@dataclass
class GameState:
    character: str
    surface: str
    menu_theme: str
    screen_width: int
    screen_height: int


@dataclass
class CharacterState:
    character_id: int = None
    name: str = None
    fishing_experience: int = None
    age: int = None
    strength: int = None
    max_stamina: int = None
    stamina: int = None
    gear: list = field(default_factory=list)
    boats: list = field(default_factory=list)


GameState = namedtuple("GameState", ["character_state", "battle_state", "world_state"])


def is_pickleable(obj, depth=0):  # DEBUG REMOVE ME
    try:
        pickle.dumps(obj)
        return True
    except TypeError as e:
        print("  " * depth + f"Failed in {type(obj)}: {e}")
        if hasattr(obj, "__dict__"):
            for key, val in obj.__dict__.items():
                print("  " * depth + f"Checking attribute {key} of type {type(val)}")
                is_pickleable(val, depth + 1)
        return False


class StateManager:
    @staticmethod
    def save_state(path, *states):
        for state in states:
            is_pickleable(state)  # DEBUG REMOVE ME
        with open(f"saved_data/{path}", "wb") as f:
            pickle.dump(states, f)

    @staticmethod
    def load_state(path):
        with open(f"saved_data/{path}", "rb") as f:
            states = pickle.load(f)

            return GameState(*states)
            # return pickle.load(f)
            # character_state, battle_state, world_state = pickle.load(f)
            # return character_state, battle_state, world_state

    @staticmethod
    def apply_state(source, target):
        for field in fields(target):
            if hasattr(source, field.name):
                setattr(target, field.name, getattr(source, field.name))
