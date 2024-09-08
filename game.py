from character import Character
from boat import Boat
from garage import Garage
from battle import Battle, Cast
from locations import *
from bait import *
from rods import *
from util import *
from fish import *
from state_manager import StateManager, WorldState, CharacterState, BattleState
import os
import pygame_menu
import pygame
import sys
import pygame_gui

from pygame_gui.elements import UIButton, UITextEntryLine
from pygame_gui import UIManager



pygame.init()
clock = pygame.time.Clock()
surface = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF)
pygame.display.set_caption('Fishing RPG')
menu_theme = pygame_menu.themes.THEME_DARK.copy()
menu_theme.title_offset = (5, -2)
menu_theme.widget_font_size = 25
state_manager = StateManager()

def game_interface(character):

    menu = pygame_menu.Menu('Game Menu', 800, 600, theme=menu_theme)

    menu.add.label(f"Welcome {character.name}!", max_char=-1, font_size=30)
    menu.add.button('Show Stats', display_stats, character)
    menu.add.button('Show Equipment', display_equipment, character)
    menu.add.button('Go Fishing', choose_location, character, surface, menu_theme)
    menu.add.button('Test', test, character)
    menu.add.button('Quit', pygame_menu.events.EXIT)

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

def main_menu():
    # menu_theme = pygame_menu.themes.THEME_DARK.copy()
    # menu_theme.title_offset = (5, -2)
    # menu_theme.widget_font_size = 25
    menu = pygame_menu.Menu('Game Menu', 800, 600, theme=menu_theme)

    menu.add.button('Load Game', load_game)
    menu.add.button('New Game', start_new_game)
    menu.add.button('Quit', pygame.quit)
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
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
            state_manager.save_state(f"{character_id}.pkl", new_character, battle, world)
            print("Starting a new game...")
            game_interface(new_character)

    menu = pygame_menu.Menu('New Game', 800, 600, theme=menu_theme)
    menu.add.label("Enter a Name:")
    name_entry = menu.add.text_input('', default='')
    menu.add.button('Confirm', lambda: begin_game(name_entry.get_value()))
    menu.add.button('Cancel', pygame_menu.events.BACK)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
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
    # # surface = pygame.display.set_mode((800, 600))
    # menu_theme = pygame_menu.themes.THEME_DARK.copy()
    # menu_theme.title_offset = (5, -2)
    # menu_theme.widget_font_size = 25
    menu = pygame_menu.Menu('Load Game', 800, 600, theme=menu_theme)

    if saved_files:
        # print("\nSaved games:")
        for file in saved_files:
            with open(f"saved_data/{file}", "rb") as f:
                character_state, _, _ = pickle.load(f)
                character_names.append(character_state.name)

        def load_selected_game(menu, save_file):
            character_state, battle_state, world_state = state_manager.load_state(save_file)
            character_data = generate_default_character_data()
            dummy_character = Character(**character_data)
            state_manager.apply_state(character_state, dummy_character)
            print(f"Loaded game: {dummy_character.name}")
            # game = Game()
            # game.play_game(dummy_character)
            game_interface(dummy_character)

        menu = pygame_menu.Menu('Choose a Saved Game', 600, 400, theme=pygame_menu.themes.THEME_DARK)

        for file, name in zip(saved_files, character_names):
            menu.add.button(name, load_selected_game, menu, file)

        menu.add.button('Back', pygame_menu.events.BACK)
    else:
        menu = pygame_menu.Menu('No Saved Games Available', 600, 400, theme=pygame_menu.themes.THEME_DARK)
        menu.add.label('No games to load')
        menu.add.button('Back', pygame_menu.events.BACK)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame_menu.events.BACK:
                main_menu()

        if menu.is_enabled():
            menu.update(events)
            menu.draw(surface)

        pygame.display.update()


def main_menu():
    surface = pygame.display.set_mode((800, 600))
    menu_theme = pygame_menu.themes.THEME_DARK.copy()
    menu_theme.title_offset = (5, -2)
    menu_theme.widget_font_size = 25
    menu = pygame_menu.Menu('Game Menu', 800, 600, theme=menu_theme)

    menu.add.button('Load Game', load_game)
    menu.add.button('New Game', start_new_game)
    menu.add.button('Quit', exit)
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        if menu.is_enabled():
            menu.update(events)
            menu.draw(surface)

        pygame.display.update()



# Initialize Pygame
# pygame.init()
# clock = pygame.time.Clock()
# clock.tick(60)
# screen = pygame.display.set_mode((800, 600))

while True:
    clock.tick(60)
    main_menu()

pygame.quit()
sys.exit()









# class Game:
#     def __init__(self):
#         self.current_character = None
#
#     def play_game(self, character):
#         try:
#             self.current_character = character
#             print(f"\nWelcome {character.name}!")
#             while True:
#                 print("\n1. Show Stats")
#                 print("2. Show Equipment")
#                 print("3. Go Fishing!")
#                 print("4. TEST")
#                 choice = input()
#                 if choice == "1":
#                     display_stats(character)
#                 elif choice == "2":
#                     display_equipment(character)
#                 elif choice == "3":
#                     go_fishing(character)
#                 elif choice == "4":
#                     test(character)
#
#         except KeyboardInterrupt:
#             print("Exiting now. Bye!")
#             exit()
#
#
# state_manager = StateManager()
#
#
# def start_new_game():
#     while True:
#         choice = input("Enter a name for your new character:\n")
#         break
#     character_data = generate_default_character_data(choice=choice)
#     character_id = character_data.get("character_id")
#     new_character = Character(**character_data)
#
#     battle = BattleState()
#     world = World()
#
#     state_manager.save_state(f"{character_id}.pkl", new_character, battle, world)
#
#     print("Starting a new game...")
#     game = Game()
#     game.play_game(new_character)
#     # self.play_game(new_character)
#
#
# def load_game():
#     saved_files = [f for f in os.listdir("saved_data") if f.endswith(".pkl")]
#     character_names = []
#
#     if saved_files:
#         print("\nSaved games:")
#         for file in saved_files:
#             with open(f"saved_data/{file}", "rb") as f:
#                 character_state, _, _ = pickle.load(f)
#                 character_names.append(character_state.name)
#
#         while True:
#             for i, name in enumerate(character_names, start=1):
#                 print(f"{i}. {name}")
#             try:
#                 save_index = int(input("\nEnter the index of the save to load: ")) - 1
#                 if 0 <= save_index < len(saved_files):
#                     save_file = saved_files[save_index]
#                     character_state, battle_state, world_state = (
#                         state_manager.load_state(save_file)
#                     )
#
#                     character_data = generate_default_character_data()
#                     dummy_character = Character(**character_data)
#
#                     state_manager.apply_state(character_state, dummy_character)
#
#                     print(f"\nLoaded game: {character_names[save_index]}")
#                     game = Game()
#                     game.play_game(dummy_character)
#                     # self.play_game()
#                     break
#             except (ValueError, IndexError):
#                 print("\nInvalid choice. Try again:\n")
#     else:
#         print("No saved games available.")
#
#
# def main_menu():
#     while True:
#         choice = input(
#             "Enter 'L' to load a game, 'N' to start a new game, or 'Q' to quit: "
#         ).upper()
#         if choice == "L":
#             load_game()
#             break
#         elif choice == "N":
#             start_new_game()
#             break
#         elif choice == "Q":
#             # self.exit_game()
#             break
#         else:
#             print("Invalid choice, please try again.")


# main_menu()
