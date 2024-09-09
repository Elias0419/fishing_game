from dataclasses import dataclass, field, fields
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


class StateManager:
    @staticmethod
    def save_state(path, *states):
        with open(f"saved_data/{path}", "wb") as f:
            pickle.dump(states, f)

    @staticmethod
    def load_state(path):
        with open(f"saved_data/{path}", "rb") as f:
            return pickle.load(f)
            # character_state, battle_state, world_state = pickle.load(f)
            # return character_state, battle_state, world_state

    @staticmethod
    def apply_state(source, target):
        for field in fields(target):
            if hasattr(source, field.name):
                setattr(target, field.name, getattr(source, field.name))
