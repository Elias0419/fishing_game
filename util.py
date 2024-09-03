import pickle
import os
import random


def create_level_map():
    return {x: 100 * 2 ** (x - 10) for x in range(10, 101)}


def load_save_data(character_id):
    save_path = f"saved_data/{character_id}.pkl"
    if os.path.exists(save_path):
        with open(save_path, "rb") as file:
            data = pickle.load(file)
            return data
    else:
        return None


def save_data(character):
    if not os.path.exists("saved_data"):
        os.makedirs("saved_data")
    save_path = f"saved_data/{character.character_id}.pkl"
    with open(save_path, "wb") as file:
        pickle.dump(character, file)
        print(f"Data saved for character ID: {character.character_id}.")


def generate_character_id():
    id = random.randint(1000000, 10000000)  # maybe prevent collisions, but probably not
    return id


def get_level_from_experience(experience):
    level_map = create_level_map()
    for level in sorted(level_map.keys(), reverse=True):
        if experience >= level_map[level]:
            return level
    return 10
