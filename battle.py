import random
import math
from util import get_level_from_experience


class Battle:
    def __init__(self):
        pass

    def battle_fish(self, character, fish, bait, difficulty=None):
        player_stamina = character.stamina
        fish_stamina = fish.stamina
        while True:
            if difficulty == None:
                if self.none_battle(difficulty, character, fish, bait):
                    break
            elif difficulty == "easy":
                if self.easy_battle(difficulty, character, fish, bait):
                    break
            elif difficulty == "medium":
                if self.medium_battle(difficulty, character, fish, bait):
                    break
            elif difficulty == "hard":
                if self.hard_battle(difficulty, character, fish, bait):
                    break
            elif difficulty == "impossible":
                if self.impossible_battle(difficulty, character, fish, bait):
                    break

    # def print_battle_stamina(self, character, fish):
    #     print(f"{character.name} stamina: {character.stamina}")
    #     print(f"Fish stamina: {fish.stamina}")

    def print_battle_menu(self, difficulty, character, fish, bait):
        while True:
            print(f"{character.name} stamina: {character.stamina}")
            print(f"Fish stamina: {fish.stamina}\n")
            print("\nBattle Menu")
            print("'Enter' To Reel")
            print("'R' To Let The Fish Take Line")
            print("'A' To Adjust Drag")
            print("'O' For Other Options")
            print("'Q' To Cut Your Line")
            choice = input()
            if choice.lower() == "":
                if self.reel(difficulty, character, fish, bait):
                    print("You've successfully reeled in the fish!")
                    return True

    def easy_battle(self, difficulty, character, fish, bait):
        # self.print_battle_stamina(character, fish)
        if self.print_battle_menu(difficulty, character, fish, bait):
            return True

    def medium_battle(self, difficulty, character, fish, bait):
        print("medium_battle")

    def hard_battle(self, difficulty, character, fish, bait):
        print("hard_battle")

    def impossible_battle(self, difficulty, character, fish, bait):
        print("impossible_battle")

    def none_battle(self, difficulty, character, fish, bait):
        print(
            "\nThis fish feels like a lightweight. \nPress Enter to try to reel it in, or type 'O' for other options, or 'Q' to cut your line and give up.\n"
        )
        choice = input()
        if choice == "":
            if self.check_win(difficulty, character, fish, bait):
                return True
            else:
                print("Try again logic goes here")  # TODO

    def reel(self, difficulty, character, fish, bait):

        if self.check_win(difficulty, character, fish, bait):
            return True
        else:
            self._TESTING_(character)
            if self.calculate_char_stamina_loss(difficulty, character, fish, bait):
                return True
            elif self.calculate_fish_stamina_loss(difficulty, character, fish, bait):
                return True

            return False

    def _TESTING_(self, character): # TODO REMOVE ME
        character.stamina = 100


    def calculate_char_stamina_loss(self, difficulty, character, fish, bait):
        rounded_fish_weight = math.ceil(fish.weight_lbs)
        experience_gap = fish.minimum_fishing_experience - character.fishing_experience
        char_stamina_loss = rounded_fish_weight + random.randint(int(experience_gap / 4), experience_gap)
        character.stamina -= char_stamina_loss
        print(f"You used {char_stamina_loss} stamina!")

    def calculate_fish_stamina_loss(self, difficulty, character, fish, bait, weight='normal'):
        if weight == 'high':
            percent_loss = random.randint(50, 90)
        elif weight == 'low':
            percent_loss = random.randint(10, 50)
        else:
            percent_loss = random.randint(10, 90)

        stamina_loss = max(1, round(fish.stamina * percent_loss / 100))


        if fish.stamina - stamina_loss <= 0:
            fish.stamina = 0
            self.end_battle(difficulty, character, fish, bait)
            print(f"The fish has exhausted all its stamina and the battle ends.")
            return True
        else:
            fish.stamina -= stamina_loss
            print(f"The fish used {stamina_loss} stamina!") # TODO figure out what to do with fractional stamina
            return False

    def check_win(self, difficulty, character, fish, bait):
        if difficulty == None:
            if self.random_chance(90):
                self.end_battle(difficulty, character, fish, bait)

                return True
            else:
                print("doh")  # TODO
                return False
        elif difficulty == "easy":
            if self.random_chance(1):
                self.end_battle(difficulty, character, fish, bait)
                return True
            else:
                return False

    def end_battle(self, difficulty, character, fish, bait):
        exp = fish.gives_exp
        # character.fishing_experience += exp # TODO testing
        print("exp increase disabled for testing")
        old_age = character.age
        new_age = get_level_from_experience(character.fishing_experience)
        if new_age != old_age:
            print("age increased")
        self.print_battle_summary(difficulty, character, fish, bait, exp)

    def print_battle_summary(self, difficulty, character, fish, bait, exp):
        print(
            f"You caught a {fish.name}!\nDifficulty: {difficulty}\nLength: {fish.length_inch:.2f} inches\nWeight: {fish.weight_lbs:.2f} pounds\n\nYou gained {exp} fishing experience!"
        )

    def random_chance(self, percent):
        return random.random() < percent / 100


class Cast:
    def __init__(self):
        pass

    def cast_line(self, character, fish, bait, location=None):
        self.bite(
            character, fish, bait
        )  # TODO lots of casting logic, this is for testing

    def bite(self, character, fish, bait):
        if character.fishing_experience < fish.minimum_fishing_experience:
            self.level_too_low(character, fish, bait)
        else:
            if fish.eats == ["all"]:
                battle = Battle()
                battle.battle_fish(character, fish, bait)
            elif bait.name in fish.eats:
                battle = Battle()
                battle.battle_fish(character, fish, bait)
            else:
                self.wrong_bait_message()

    def wrong_bait_message(self):
        messages = [
            "\nYou felt a bump, but nothing. Maybe the bait is wrong?",
            "\nJust a nibble and then silence...",
            "\nThe line twitches briefly... the fish don't seem interested in this bait.",
            "\nNothin'...",
            "\nYou wait and wait... seems like the fish aren't biting this one.",
            "\nA small tug on the line, then nothing.",
        ]
        print(random.choice(messages))

    def level_too_low(self, character, fish, bait):
        print("\nYou hooked a big one!")
        if character.fishing_experience * 2 >= fish.minimum_fishing_experience:
            print("\nIt feels like you have a fair chance to beat this one.")
            self.continue_or_quit("easy", character, fish, bait)
        elif character.fishing_experience * 3 >= fish.minimum_fishing_experience:
            print("\nIt feels pretty hefty!")
            self.continue_or_quit("medium", character, fish, bait)
        elif character.fishing_experience * 4 >= fish.minimum_fishing_experience:
            print("\nYou can tell this is gonna be a tough fight.")
            self.continue_or_quit("hard", character, fish, bait)

        else:
            print(
                "\nThere's no way you're gonna reel this beast in! Quit while you can!"
            )
            self.continue_or_quit("impossible", character, fish, bait)

    def continue_or_quit(self, difficulty, character, fish, bait):

        choice = input(
            "\nPress Enter to fight the fish, or type 'Q' and press Enter to cut the line and give up.\n"
        )
        if choice == "":
            battle = Battle()
            battle.battle_fish(character, fish, bait, difficulty)
        elif choice == "Q".lower():
            pass # TODO cutting line penalty?

    def give_up(self):
        pass
