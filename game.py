from character import Character
from boat import Boat
from garage import Garage
from battle import Battle, Cast
from locations import *
from bait import *
from rods import *
from util import *
from fish import *

import os


class Game:
    def __init__(self):
        self.current_character = None
        self.level_map = create_level_map()

        self.locations = [NeighborhoodPond(), StreamInTheWoods()]
        # self.main_menu()
        try:
            self.main_menu()
        except KeyboardInterrupt:
            self.exit_game()

    def exit_game(self):
        if self.current_character:
            save_data(self.current_character)
        print("Exiting game. Bye!")

    def main_menu(self):
        while True:
            choice = input(
                "Enter 'L' to load a game, 'N' to start a new game, or 'Q' to quit: "
            ).upper()
            if choice == "L":
                self.load_game()
                break
            elif choice == "N":
                self.start_new_game()
                break
            elif choice == "Q":
                self.exit_game()
                break
            else:
                print("Invalid choice, please try again.")

    def load_game(self):
        saved_files = [
            f.replace(".pkl", "")
            for f in os.listdir("saved_data")
            if f.endswith(".pkl")
        ]
        if saved_files:
            print("\nSaved games:")
            while True:
                for i, file in enumerate(saved_files, start=1):
                    with open(f"saved_data/{file}.pkl", "rb") as f:
                        character_data = pickle.load(f)
                        print(i, character_data.name)
                try:
                    char_index = int(
                        input("\nEnter the index of the character to load: ")
                    )
                    char_id = saved_files[char_index - 1]
                    with open(f"saved_data/{char_id}.pkl", "rb") as f:
                        data = pickle.load(f)

                    character = Character(data, data.character_id)
                    self.current_character = character
                    print(f"\nLoaded {character.name}")
                    self.play_game(character)
                    break
                except (ValueError, IndexError):
                    print("\nInvalid Choice\nTry Again:\n")

        else:
            print("No saved games available.")
            self.start_new_game()

    def available_locations(self, player_level: int) -> list[Location]:
        return [loc for loc in self.locations if player_level >= loc.minimum_level]

    def choose_location(self, player_level: int) -> Location:

        available = self.available_locations(player_level)
        while True:
            if available:
                print("\n")
                for i, location in enumerate(available, 1):
                    print(f"{i}. {location.name}")
                try:
                    choice = int(input("\nChoose a location by number:\n "))
                    return available[choice - 1]
                except (ValueError, IndexError):
                    print("\nInvalid Choice\nTry Again:")

    def start_new_game(self):
        while True:
            choice = input("Enter a name for your new character:\n")
            break
        character_id = generate_character_id()
        character_data = {
            "character_id": character_id,
            "name": choice,
            "age": 10,
            "fishing_experience": 6,  # Test
            # "fishing_experience": 0,
            "strength": 1,
            "stamina": 100,
            "max_stamina": 100,
            "gear": [{"rod": Twig(TenLbMono(), Reel()), "bait": Worm(amount=10)}],
            "boats": [],
        }
        new_character = Character(
            character_data, character_id=character_data.get("character_id")
        )
        save_data(new_character)
        self.current_character = new_character
        print("Starting a new game...")
        self.play_game(new_character)

    def play_game(self, character: Character):
        self.current_character = character
        print(f"\nWelcome {character.name}!")
        while True:
            print("\n1. Show Stats")
            print("2. Show Equipment")
            print("3. Go Fishing!")
            print("4. TEST")
            choice = input()
            if choice == "1":
                print(
                    f"\nName {character.name}\nAge {character.age}\nExperience {character.fishing_experience}\nStrength {character.strength}\nStamina {character.stamina}"
                )
            elif choice == "2":
                print(
                    f"\nRod:\n{character.gear[0]['rod'].name}\nHit Points: {character.gear[0]['rod'].hit_points}\nBreaking Strength (lbs): {character.gear[0]['rod'].breaking_strength_lbs}\n\nLine:\n{character.gear[0]['rod'].line.name}\n\nReel:\n{character.gear[0]['rod'].reel.name}\nMax Drag: {character.gear[0]['rod'].reel.drag_lbs}"
                )
            elif choice == "3":
                location = self.choose_location(character.fishing_experience)
                fish = location.get_fish()
                bait = character.gear[0]["bait"]
                cast = Cast()
                cast.cast_line(character, fish, bait)
            elif choice == "4":
                location = NeighborhoodPond()
                print(location.get_fish())


game = Game()
