import pickle
import os
import random

from rods import Twig, TenLbMono, Reel
from bait import Worm
from locations import Location, World, StreamInTheWoods
from state_manager import WorldState, LocationState, StateManager
from battle import Cast
import pygame
import pygame_menu

def log_output(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        update_log(result)
        return result
    return wrapper


def create_log_surface(width, height):
    log_surface = pygame.Surface((width, height))
    return log_surface

def update_log(message, log_surface, font, color=(255, 255, 255)):
    text = font.render(message, True, color)


def test(character):  # unlocking locations
    world = World.get_instance(character)
    battle = ""
    for location in world.locations:
        if location.name == "Stream in the Woods":
            location.unlocked = True
            break
    StateManager.save_state(f"{character.character_id}.pkl", character, battle, world)


def available_locations(character):
    player_level = character.age
    world = World.get_instance(character)
    _, _, world_state = StateManager.load_state(f"{character.character_id}.pkl")
    if world_state.locations != []:
        StateManager.apply_state(world_state, world)
    return [
        loc
        for loc in world.locations
        if player_level >= loc.minimum_level and loc.unlocked
    ]


def choose_location(character, surface, menu_theme):
    menu = pygame_menu.Menu('World Map', 600, 400, theme=pygame_menu.themes.THEME_DARK)
    available = available_locations(character)
    for i, location in enumerate(available, 1):
        menu.add.button(f"{i}. {location.name}", go_fishing, character, surface, menu_theme, location)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if menu.is_enabled():
            menu.update(events)
            menu.draw(surface)
        pygame.display.update()
    # while True:
    #     if available:
    #         print("\n")
    #         for i, location in enumerate(available, 1):
    #             print(f"{i}. {location.name}")
    #         try:
    #             choice = int(input("\nChoose a location by number:\n "))
    #             return available[choice - 1]
    #         except (ValueError, IndexError):
    #             print("\nInvalid Choice\nTry Again:")


def display_stats(character):
    print(
        f"\nName {character.name}\nAge {character.age}\nExperience {character.fishing_experience}\nStrength {character.strength}\nStamina {character.stamina}"
    )


def display_equipment(character):
    print(
        f"\nRod:\n{character.gear[0]['rod'].name}\nHit Points: {character.gear[0]['rod'].hit_points}\nBreaking Strength (lbs): {character.gear[0]['rod'].breaking_strength_lbs}\n\nLine:\n{character.gear[0]['rod'].line.name}\n\nReel:\n{character.gear[0]['rod'].reel.name}\nMax Drag: {character.gear[0]['rod'].reel.drag_lbs}"
    )


def go_fishing(character, surface, menu_theme, location):

    # location = choose_location(character, surface, menu_theme)
    fish = location.get_fish()
    bait = character.gear[0]["bait"]
    cast = Cast()
    cast.cast_line(character, fish, bait)


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


def generate_default_character_data(choice="dummy"):
    character_id = generate_character_id()
    character_data = {
        "character_id": character_id,
        "name": choice,
        # "age": 10,
        "fishing_experience": 6,  # Test
        # "fishing_experience": 0,
        "strength": 1,
        "stamina": 100,
        "max_stamina": 100,
        "gear": [{"rod": Twig(TenLbMono(), Reel()), "bait": Worm(amount=10)}],
        "boats": [],
    }
    return character_data
