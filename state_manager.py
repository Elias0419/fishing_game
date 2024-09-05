from dataclasses import dataclass, field
import pickle

@dataclass
class BattleState:
    pass

@dataclass
class WorldState:
    pass

@dataclass
class CharacterState:
    pass

class StateManager:
    @staticmethod
    def save_state(path, *states):
        with open(path, 'wb') as f:
            pickle.dump(states, f)

    @staticmethod
    def load_state(path):
        with open(path, 'rb') as f:
            return pickle.load(f)
