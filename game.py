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


class Game:
    def __init__(self):
        self.current_character = None

    def play_game(self, character: Character):
        try:
            self.current_character = character
            print(f"\nWelcome {character.name}!")
            while True:
                print("\n1. Show Stats")
                print("2. Show Equipment")
                print("3. Go Fishing!")
                print("4. TEST")
                choice = input()
                if choice == "1":
                    display_stats(character)
                elif choice == "2":
                    display_equipment(character)
                elif choice == "3":
                    go_fishing(character)
                elif choice == "4":
                    test(character)

        except KeyboardInterrupt:
            print("Exiting now. Bye!")
            exit()


state_manager = StateManager()


def start_new_game():
    while True:
        choice = input("Enter a name for your new character:\n")
        break
    character_data = generate_default_character_data(choice=choice)
    character_id = character_data.get("character_id")
    new_character = Character(**character_data)

    battle = BattleState()
    world = World()

    state_manager.save_state(f"{character_id}.pkl", new_character, battle, world)

    print("Starting a new game...")
    game = Game()
    game.play_game(new_character)
    # self.play_game(new_character)


def load_game():
    saved_files = [f for f in os.listdir("saved_data") if f.endswith(".pkl")]
    character_names = []

    if saved_files:
        print("\nSaved games:")
        for file in saved_files:
            with open(f"saved_data/{file}", "rb") as f:
                character_state, _, _ = pickle.load(f)
                character_names.append(character_state.name)

        while True:
            for i, name in enumerate(character_names, start=1):
                print(f"{i}. {name}")
            try:
                save_index = int(input("\nEnter the index of the save to load: ")) - 1
                if 0 <= save_index < len(saved_files):
                    save_file = saved_files[save_index]
                    character_state, battle_state, world_state = (
                        state_manager.load_state(save_file)
                    )

                    character_data = generate_default_character_data()
                    dummy_character = Character(**character_data)

                    state_manager.apply_state(character_state, dummy_character)

                    print(f"\nLoaded game: {character_names[save_index]}")
                    game = Game()
                    game.play_game(dummy_character)
                    # self.play_game()
                    break
            except (ValueError, IndexError):
                print("\nInvalid choice. Try again:\n")
    else:
        print("No saved games available.")


def main_menu():
    while True:
        choice = input(
            "Enter 'L' to load a game, 'N' to start a new game, or 'Q' to quit: "
        ).upper()
        if choice == "L":
            load_game()
            break
        elif choice == "N":
            start_new_game()
            break
        elif choice == "Q":
            # self.exit_game()
            break
        else:
            print("Invalid choice, please try again.")


main_menu()
