import random
import math
from util import get_level_from_experience


class Battle:
    def __init__(self):
        self.drag_too_high_count = 0
        self.max_safe_drag = 0

    def battle_fish(self, character, fish, bait, difficulty=None):
        # player_stamina = character.stamina
        # fish_stamina = fish.stamina
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
        pre_battle_fish_stamina = fish.stamina
        while True:
            print(f"\n{character.name} stamina: {character.stamina}")
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
                    return True
            elif choice.lower() == "r":
                self.let_the_fish_take_line(difficulty, character, fish, bait, pre_battle_fish_stamina)
            elif choice.lower() == "a":
                adjustment, adjustment_direction = self.adjust_drag(character)
                self.calculate_drag(difficulty, character, fish, bait, adjustment=adjustment, adjustment_direction=adjustment_direction)

    def check_integer(self, input):
        try:
            int(input)
            return True
        except ValueError:
            return False

    def adjust_drag(self, character):
        reel = character.gear[0]["rod"].reel
        reel_name = reel.name
        reel_max_drag = reel.max_drag
        reel_current_drag = reel.drag_lbs


        print(f"\nThe {reel_name} has a maximum drag of {reel_max_drag} lbs.\nIt's currently set to {reel_current_drag} lbs.")

        while True:
            choice = input(f"Set the drag by entering a number less than or equal to {reel_max_drag} lbs:\n")
            if self.check_integer(choice):
                choice = int(choice)
                if choice > reel_max_drag:
                    print(f"{reel_name} can only go up to {reel_max_drag} lbs.")
                elif choice == reel_current_drag:
                    print(f"{reel_name} is already set to {choice} lbs.")
                else:
                    adjustment_direction = "up" if choice > reel_current_drag else "down"
                    adjustment = abs(reel_current_drag - choice)
                    reel.drag_lbs = choice
                    print(f"{reel_name} set to {reel.drag_lbs} lbs.")
                    return adjustment, adjustment_direction


            else:
                print("Please enter a valid number.")




    def calculate_drag(self, difficulty, character, fish, bait, adjustment=0, adjustment_direction=None):
        reel = character.gear[0]["rod"].reel
        fish_weight = fish.weight_lbs
        line_strength = character.gear[0]["rod"].line.breaking_strength_lbs
        reel_max_drag = reel.max_drag
        reel_current_drag = reel.drag_lbs
        baseline_max_safe_drag = int(min(line_strength, reel_max_drag) * 0.8)

        print("\nInside calculate_drag\nMax:", reel_max_drag, "\nCurrent", reel_current_drag, "\nAdjustment", adjustment, "\nDirection", adjustment_direction)

        if adjustment and adjustment_direction == "down":
            current_safe_drag = self.max_safe_drag
            self.max_safe_drag = current_safe_drag + adjustment
        elif adjustment and adjustment_direction == "up":
            current_safe_drag = self.max_safe_drag
            self.max_safe_drag = current_safe_drag - adjustment

        else:
            self.max_safe_drag = baseline_max_safe_drag

        minimum_effective_drag = int(max(0.5 * fish_weight, baseline_max_safe_drag * 0.5)) # * difficulty # Character skill here probably

        print("Minimum effective drag:", minimum_effective_drag, "\nMaximum safe drag:", self.max_safe_drag)

        if fish_weight > self.max_safe_drag:
            print(f"{reel.name} screams under the weight of the fish!\nReduce the drag before something breaks!")
            self.drag_too_high()
        else:
            self.drag_too_high_count = 0
            print("\nDrag too high reset to", self.drag_too_high_count, "inside calculate_drag")
            if minimum_effective_drag > reel_current_drag:
                print("\nLow drag\n")



    def drag_too_high(self):
        self.drag_too_high_count += 1
        if self.drag_too_high_count == 2 and self.random_chance(10):
            print("\ndrag_too_high set to", self.drag_too_high_count, "inside drag_too_high, if 1")
            pass  # 10% chance to break something
        elif self.drag_too_high_count == 3 and self.random_chance(25):
            print("\ndrag_too_high set to", self.drag_too_high_count, "inside drag_too_high, if 2")
            pass  # 25% chance to break something
        elif self.drag_too_high_count >= 4 and self.random_chance(50):
            print("\ndrag_too_high set to", self.drag_too_high_count, "inside drag_too_high, if 3")
            pass  # 50% chance to break something




    def let_the_fish_take_line(self, difficulty, character, fish, bait, pre_battle_fish_stamina):
        # print("take line")  # TODO maybe certain fish take line differently or stamina loss affects them differently
        if fish.stamina <= pre_battle_fish_stamina * 0.2:
            print("\nThe fish seems too weak to take any line\n")
            self.take_line_stamina_increase(character, fish_low_stamina=True)
        else:  # TODO different fish weights and gear affect how the line is pulled
            # gear damage could be here too
            # needs more complex logic for calculating loss and gain
            percent_loss = random.randint(10, 50)
            fish_stamina_loss = round(fish.stamina * percent_loss / 100)
            print(f"\nThe fish takes line. Your {character.gear[0]['rod'].reel.name} squeals under the pressure.")
            fish.stamina -= fish_stamina_loss
            print(f"The fish used {fish_stamina_loss} stamina.")
            self.take_line_stamina_increase(character)


    def take_line_stamina_increase(self, character, fish_low_stamina=False):

        if character.stamina >= character.max_stamina:
            print("You are already at maximum stamina.")
        else:
            if fish_low_stamina:
                character_stamina_gain = random.randint(1, 10)
            else:
                character_stamina_gain = random.randint(10, 50)
            new_stamina = character.stamina + character_stamina_gain
            if new_stamina > character.max_stamina:
                character_stamina_gain = character.max_stamina - character.stamina
                character.stamina = character.max_stamina
                print(f"You gained {character_stamina_gain} stamina, reaching your maximum stamina.")
            else:
                character.stamina += character_stamina_gain
                print(f"You gained {character_stamina_gain} stamina.")

    def easy_battle(self, difficulty, character, fish, bait):
        # self.print_battle_stamina(character, fish)
        print("\ndrag_too_high easy_battle before", self.drag_too_high_count)
        self.drag_too_high_count = 0
        print("drag_too_high easy_battle after", self.drag_too_high_count)

        if self.print_battle_menu(difficulty, character, fish, bait):
            return True

    def medium_battle(self, difficulty, character, fish, bait):
        self.drag_too_high_count = 0
        print("medium_battle")
        return True
    def hard_battle(self, difficulty, character, fish, bait):
        self.drag_too_high_count = 0
        print("hard_battle")
        return True
    def impossible_battle(self, difficulty, character, fish, bait):
        self.drag_too_high_count = 0
        print("impossible_battle")
        return True
    def none_battle(self, difficulty, character, fish, bait):
        print(
            "\nThis fish feels like a lightweight. \nPress Enter to try to reel it in, or type 'O' for other options, or 'Q' to cut your line and give up.\n"
        )
        choice = input()
        if choice == "":
            if self.check_win(difficulty, character, fish, bait):
                return True
            else:
                self.lose_bait(difficulty, character, fish, bait)
                # print(character.gear[0]["bait"])
                # print("Try again logic goes here")  # TODO

    def lose_bait(self, difficulty, character, fish, bait):
        # TODO more complex bait logic
        # chance = self.random_chance(50)
        # print(chance)
        if self.random_chance(50):
            bait.amount -= 1
            print(f"You lost a {bait.name}\n{bait.amount} remaining")
        else:
            print("\nYou didn't lose your bait this time.\n")

    def reel(self, difficulty, character, fish, bait):
        self.calculate_drag(difficulty, character, fish, bait)
        if self.check_win(difficulty, character, fish, bait):
            return True
        else:
            # self._TESTING_(character)
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

        # stamina_loss = max(1, round(fish.stamina * percent_loss / 100)) # TEST
        stamina_loss = round(fish.stamina * percent_loss / 100)

        if fish.stamina - stamina_loss <= 0:
            fish.stamina = 0
            self.end_battle(difficulty, character, fish, bait)
            # print(f"The fish has exhausted all its stamina and the battle ends.")
            return True
        else:
            fish.stamina -= stamina_loss
            print(f"The fish used {stamina_loss} stamina!") # TODO figure out what to do with fractional stamina
            return False

    def check_win(self, difficulty, character, fish, bait):
        if difficulty == None:
            if self.random_chance(90): # TEST
                self.end_battle(difficulty, character, fish, bait)

                return True
            else:
                # print("doh")  # TODO
                return False
        elif difficulty == "easy":
            if self.random_chance(1): # TEST
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
        print("\nYou hooked a big one!") # creating difficulties here that get passed through the battle functions
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
