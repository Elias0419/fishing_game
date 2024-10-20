import os
import pickle
import sys


import pygame
pygame.init()
import pygame_menu

from conf import init, get_globals
init()

from character import Character
from locations import World
from util import (
    generate_default_character_data,
)
from world_map import choose_location
from state_manager import StateManager, BattleState
state_manager = StateManager()

clock, screen_width, screen_height, surface, menu_theme, font, global_log = get_globals()



def game_interface(character):

    menu = pygame_menu.Menu("Game Menu", screen_width, screen_height, theme=menu_theme)

    menu.add.label(f"Welcome {character.name}!", max_char=-1, font_size=30)
    # menu.add.button("Show Stats", display_stats, character)
    # menu.add.button("Show Equipment", display_equipment, character)
    menu.add.button(
        "Go Fishing",
        choose_location, character
    )
    # menu.add.button("Test", test, character)
    menu.add.button("Quit", pygame_menu.events.EXIT)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()

        if menu.is_enabled():
            menu.update(events)
            menu.draw(surface)
        pygame.display.update()


def main_menu():

    menu = pygame_menu.Menu("Game Menu", screen_width, screen_height, theme=menu_theme)

    menu.add.button("Load Game", load_game)
    menu.add.button("New Game", start_new_game)
    menu.add.button("Quit", pygame.quit)
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()

        if menu.is_enabled():
            menu.update(events)
            menu.draw(surface)
        pygame.display.update()


def start_new_game():
    def begin_game(name):
        if name:
            character_data = generate_default_character_data(choice=name)
            character_id = character_data.get("character_id")
            new_character = Character(**character_data)
            battle = BattleState()
            world = World()
            state_manager.save_state(
                f"{character_id}.pkl", new_character, battle, world
            )
            print("Starting a new game...")
            game_interface(new_character)

    menu = pygame_menu.Menu("New Game", screen_width, screen_height, theme=menu_theme)
    menu.add.label("Enter a Name:")
    name_entry = menu.add.text_input("", default="")
    menu.add.button("Confirm", lambda: begin_game(name_entry.get_value()))
    menu.add.button("Cancel", pygame_menu.events.BACK)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    begin_game(name_entry.get_value())
                    return

        if menu.is_enabled():
            menu.update(events)
            menu.draw(surface)

        pygame.display.update()


def load_game():
    saved_files = [f for f in os.listdir("saved_data") if f.endswith(".pkl")]
    character_names = []

    menu = pygame_menu.Menu("Load Game", screen_width, screen_height, theme=menu_theme)

    if saved_files:
        # print("\nSaved games:")
        for file in saved_files:
            with open(f"saved_data/{file}", "rb") as f:
                states = pickle.load(f)
                # print(states) # DEBUG
                character_state, _, _ = states
                character_names.append(character_state.name)

        def load_selected_game(menu, save_file):
            character_state, battle_state, world_state = state_manager.load_state(
                save_file
            )
            character_data = generate_default_character_data()
            dummy_character = Character(**character_data)
            state_manager.apply_state(character_state, dummy_character)
            # print(f"Loaded game: {dummy_character.name}") # DELETE ME

            game_interface(dummy_character)

        menu = pygame_menu.Menu(
            "Choose a Saved Game", screen_width, screen_height, theme=menu_theme
        )

        for file, name in zip(saved_files, character_names):
            menu.add.button(name, load_selected_game, menu, file)

        menu.add.button("Back", pygame_menu.events.BACK)
    else:
        menu = pygame_menu.Menu(
            "No Saved Games Available", screen_width, screen_height, theme=menu_theme
        )
        menu.add.label("No games to load")
        menu.add.button("Back", pygame_menu.events.BACK)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame_menu.events.BACK:
                main_menu()

        if menu.is_enabled():
            menu.update(events)
            menu.draw(surface)

        pygame.display.update()


def main_menu():

    menu = pygame_menu.Menu("Game Menu", screen_width, screen_height, theme=menu_theme)

    menu.add.button("Load Game", load_game)
    menu.add.button("New Game", start_new_game)
    menu.add.button("Quit", exit)
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()

        if menu.is_enabled():
            menu.update(events)
            menu.draw(surface)

        pygame.display.update()


while True:
    clock.tick(30)
    main_menu()

pygame.quit()
sys.exit()
