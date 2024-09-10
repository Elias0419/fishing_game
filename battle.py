import random
import math
from state_manager import StateManager, WorldState, CharacterState, BattleState
from locations import World
import pygame
import pygame_menu
from collections import deque
from functools import wraps
from contextlib import redirect_stdout
import io
from textwrap import wrap
class CombatLog:
    def __init__(self, x, y, width, height, font, surface):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.surface = surface
        self.messages = deque(maxlen=200)
        self.offset = 0

    def add_message(self, message):
        lines = message.split('\n')
        for line in lines:  # Reverse to maintain the correct order when displaying
            self.messages.appendleft(line)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                self.offset -= 1
            elif event.button == 5:  # Scroll down
                self.offset += 1

            # Clamp the offset to prevent scrolling beyond the content
            self.offset = max(0, min(self.offset, len(self.messages) - (self.rect.height // 20)))

    def draw(self):
        self.surface.fill((0, 0, 0), self.rect)
        start_y = self.rect.bottom - 20
        for i in range(self.offset, len(self.messages)):
            try:
                message = self.messages[i]
                text_surf = self.font.render(message, True, (255, 255, 255))
                self.surface.blit(text_surf, (self.rect.x + 5, start_y))
                start_y -= 20
                if start_y < self.rect.top:
                    break
            except IndexError:
                pass

class LogDecorator:
    def __init__(self, log_attribute):
        self.log_attribute = log_attribute

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.__class__(getattr(instance, self.log_attribute))

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            str_buffer = io.StringIO()
            with redirect_stdout(str_buffer):
                result = func(*args, **kwargs)
            output = str_buffer.getvalue()
            log_instance = getattr(args[0], self.log_attribute)
            if output:
                log_instance.add_message(output.strip())
            return result
        return wrapper


def create_level_map():
    return {x: 100 * 2 ** (x - 10) for x in range(10, 101)}


def get_level_from_experience(experience):
    level_map = create_level_map()
    for level in sorted(level_map.keys(), reverse=True):
        if experience >= level_map[level]:
            return level
    return 10


class Battle:
    def __init__(self, combat_log):
        self.drag_too_high_count = 0
        self.drag_too_low_count = 0
        # self.drag_init_flag = False
        self.max_safe_drag = None
        self.first_round = True
        self.combat_log = combat_log

    def battle_fish(self, character, fish, bait, surface, menu_theme, location, screen_width, screen_height, difficulty):

        while True:
            if difficulty == None:
                if self.none_battle(difficulty, character, fish, bait):
                    break
            elif difficulty == "easy":
                if self.easy_battle(character, fish, bait, surface, menu_theme, location, screen_width, screen_height, difficulty):
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

    def print_battle_menu(self, character, fish, bait, surface, menu_theme, location, screen_width, screen_height, difficulty):
        pre_battle_fish_stamina = fish.stamina
        menu_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
        menu = pygame_menu.Menu("Battle", screen_width, screen_height, theme=menu_theme)
        # menu.add.button('Reel', reel_fish)
        menu.add.button('Let Fish Take Line', self.let_the_fish_take_line, difficulty, character, fish, bait, pre_battle_fish_stamina)
        menu.add.button('Adjust Drag', self.adjust_drag)
        # menu.add.button('Other Options', other_options)
        # menu.add.button('Cut Your Line', cut_line)
        menu.add.button('Quit', pygame_menu.events.EXIT)

        while True:
            # screen.fill((0, 0, 0))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:  # Scroll up
                        try:
                            self.combat_log.offset += 1
                        except IndexError:
                            pass
                    elif event.button == 5:  # Scroll down
                        try:
                            self.combat_log.offset -= 1
                        except IndexError:
                            pass

            menu.update(events)
            menu.draw(surface)
            self.combat_log.draw()
            pygame.display.flip()
        # print(character, fish, bait, surface, menu_theme, location, screen_width, screen_height, combat_log, difficulty)
        # pre_battle_fish_stamina = fish.stamina
        # while True:
        #     print(f"\n{character.name} stamina: {character.stamina}")
        #     print(f"Fish stamina: {fish.stamina}\n")
        #     print("\nBattle Menu")
        #     print("'Enter' To Reel")
        #     print("'R' To Let The Fish Take Line")
        #     print("'A' To Adjust Drag")
        #     print("'O' For Other Options")
        #     print("'Q' To Cut Your Line")
        #     choice = input()
        #     if choice.lower() == "":
        #         if self.reel(difficulty, character, fish, bait):
        #             return True
        #     elif choice.lower() == "r":
        #         self.let_the_fish_take_line(
        #             difficulty, character, fish, bait, pre_battle_fish_stamina
        #         )
        #     elif choice.lower() == "a":
        #         adjustment, adjustment_direction = self.adjust_drag(character)
        #         self.calculate_drag(
        #             difficulty,
        #             character,
        #             fish,
        #             bait,
        #             adjustment=adjustment,
        #             adjustment_direction=adjustment_direction,
        #         )

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

        print(
            f"\nThe {reel_name} has a maximum drag of {reel_max_drag} lbs.\nIt's currently set to {reel_current_drag} lbs."
        )

        while True:
            choice = input(
                f"Set the drag by entering a number less than or equal to {reel_max_drag} lbs:\n"
            )
            if self.check_integer(choice):
                choice = int(choice)
                if choice > reel_max_drag:
                    print(f"{reel_name} can only go up to {reel_max_drag} lbs.")
                elif choice == reel_current_drag:
                    print(f"{reel_name} is already set to {choice} lbs.")
                else:
                    adjustment_direction = (
                        "up" if choice > reel_current_drag else "down"
                    )
                    adjustment = abs(reel_current_drag - choice)
                    reel.drag_lbs = choice
                    print(f"{reel_name} set to {reel.drag_lbs} lbs.")
                    return adjustment, adjustment_direction

            else:
                print("Please enter a valid number.")

    def calculate_drag(
        self, difficulty, character, fish, bait, adjustment=0, adjustment_direction=None
    ):
        reel = character.gear[0]["rod"].reel
        fish_weight = fish.weight_lbs
        line_strength = character.gear[0]["rod"].line.breaking_strength_lbs
        reel_max_drag = reel.max_drag
        reel_current_drag = reel.drag_lbs
        baseline_max_safe_drag = int(min(line_strength, reel_max_drag) * 0.8)

        print(  # DEBUG remove me
            "\nInside calculate_drag\nMax:",
            reel_max_drag,
            "\nCurrent",
            reel_current_drag,
            "\nAdjustment",
            adjustment,
            "\nDirection",
            adjustment_direction,
        )

        state_manager = StateManager()
        _, battle_state, _ = state_manager.load_state(f"{character.character_id}.pkl")
        if battle_state.max_safe_drag is None:
            self.max_safe_drag = baseline_max_safe_drag
        else:
            self.max_safe_drag = battle_state.max_safe_drag

        if adjustment:
            if adjustment_direction == "down":
                self.max_safe_drag += adjustment
            elif adjustment_direction == "up":
                self.max_safe_drag -= adjustment
        world = World.get_instance()
        state_manager.save_state(
            f"{character.character_id}.pkl", character, self, world
        )
        minimum_effective_drag = int(
            max(0.5 * fish_weight, baseline_max_safe_drag * 0.5)
        )  # * difficulty # Character skill here probably

        print(  # DEBUG remove me
            "Minimum effective drag:",
            minimum_effective_drag,
            "\nMaximum safe drag:",
            self.max_safe_drag,
        )
        if fish_weight > self.max_safe_drag:
            print(
                f"{reel.name} screams under the weight of the fish!\nReduce the drag before something breaks!"
            )
            self.drag_too_high()
        else:
            self.drag_too_high_count = 0
            print(
                "\nDrag too high reset to",
                self.drag_too_high_count,
                "inside calculate_drag",
            )
            if minimum_effective_drag > reel_current_drag:
                self.drag_too_low()
            else:
                self.drag_too_low_count = 0

    def drag_too_low(self):  # probably affected by experience or skills
        self.drag_too_low_count += 1
        if self.drag_too_low_count == 1:
            print("The fish is taking line fast! The drag is too low!")
        elif self.drag_too_low_count == 2:
            print(
                "You're gonna get spooled! Tighten the drag before you run out of line!"
            )
        elif self.drag_too_low_count >= 3:
            print("You got spooled!")
            # TODO some gear loss or breakage goes here

    def drag_too_high(self):
        self.drag_too_high_count += 1
        if self.drag_too_high_count == 2 and self.random_chance(10):
            print(
                "\ndrag_too_high set to",
                self.drag_too_high_count,
                "inside drag_too_high, if 1",
            )
            pass  # 10% chance to break something
        elif self.drag_too_high_count == 3 and self.random_chance(25):
            print(
                "\ndrag_too_high set to",
                self.drag_too_high_count,
                "inside drag_too_high, if 2",
            )
            pass  # 25% chance to break something
        elif self.drag_too_high_count >= 4 and self.random_chance(50):
            print(
                "\ndrag_too_high set to",
                self.drag_too_high_count,
                "inside drag_too_high, if 3",
            )
            pass  # 50% chance to break something

    @LogDecorator('combat_log')
    def let_the_fish_take_line(
        self, difficulty, character, fish, bait, pre_battle_fish_stamina
    ):
        print("\ncombat log test")
        # print("take line")  # TODO maybe certain fish take line differently or stamina loss affects them differently
        if fish.stamina <= pre_battle_fish_stamina * 0.2:
            print("\nThe fish seems too weak to take any line\n")
            self.take_line_stamina_increase(character, fish_low_stamina=True)
        else:  # TODO different fish weights and gear affect how the line is pulled
            # gear damage could be here too
            # needs more complex logic for calculating loss and gain
            percent_loss = random.randint(10, 50)
            fish_stamina_loss = round(fish.stamina * percent_loss / 100)
            print("\nThe fish takes line.")
            print(f"\nYour {character.gear[0]['rod'].reel.name} squeals under the pressure.")
            fish.stamina -= fish_stamina_loss
            print(f"\nThe fish used {fish_stamina_loss} stamina.")
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
                print(
                    f"You gained {character_stamina_gain} stamina, reaching your maximum stamina."
                )
            else:
                character.stamina += character_stamina_gain
                print(f"You gained {character_stamina_gain} stamina.")

    def easy_battle(self, character, fish, bait, surface, menu_theme, location, screen_width, screen_height, difficulty):
        # self.print_battle_stamina(character, fish)
        print("\ndrag_too_high easy_battle before", self.drag_too_high_count)
        self.drag_too_high_count = 0
        print("drag_too_high easy_battle after", self.drag_too_high_count)

        if self.print_battle_menu(character, fish, bait, surface, menu_theme, location, screen_width, screen_height, difficulty):
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

    def _TESTING_(self, character):  # TODO REMOVE ME
        character.stamina = 100

    def calculate_char_stamina_loss(self, difficulty, character, fish, bait):
        rounded_fish_weight = math.ceil(fish.weight_lbs)
        experience_gap = fish.minimum_fishing_experience - character.fishing_experience
        char_stamina_loss = rounded_fish_weight + random.randint(
            int(experience_gap / 4), experience_gap
        )
        character.stamina -= char_stamina_loss
        print(f"You used {char_stamina_loss} stamina!")

    def calculate_fish_stamina_loss(
        self, difficulty, character, fish, bait, weight="normal"
    ):
        if weight == "high":
            percent_loss = random.randint(50, 90)
        elif weight == "low":
            percent_loss = random.randint(10, 50)
        else:
            print("default fish stamina loss")
            percent_loss = random.randint(10, 90)
            print(percent_loss)

        # stamina_loss = max(1, round(fish.stamina * percent_loss / 100)) # TEST
        stamina_loss = round(fish.stamina * percent_loss / 100)

        if fish.stamina - stamina_loss <= 0:
            fish.stamina = 0
            self.end_battle(difficulty, character, fish, bait)
            # print(f"The fish has exhausted all its stamina and the battle ends.")
            return True
        else:
            fish.stamina -= stamina_loss
            print(
                f"The fish used {stamina_loss} stamina!"
            )  # TODO figure out what to do with fractional stamina
            return False

    def check_win(self, difficulty, character, fish, bait):
        if difficulty == None:
            if self.random_chance(90):  # TEST
                self.end_battle(difficulty, character, fish, bait)

                return True
            else:
                # print("doh")  # TODO
                return False
        elif difficulty == "easy":
            if self.random_chance(1):  # TEST
                self.end_battle(difficulty, character, fish, bait)
                return True
            else:
                return False

    def end_battle(self, difficulty, character, fish, bait):
        self.drag_init_flag = False
        self.drag_too_high_count = 0
        self.drag_too_low_count = 0
        exp = fish.gives_exp
        # character.fishing_experience += exp # TODO testing
        print("exp increase disabled for testing")
        old_age = character.age
        new_age = get_level_from_experience(character.fishing_experience)
        if new_age != old_age:
            print("age increased")
        state_manager = StateManager()
        state_manager.save_state(
            f"{character.character_id}.pkl", character, self, WorldState()
        )  # dummy world state
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

    def cast_line(self, character, fish, bait, surface, menu_theme, location, screen_width, screen_height):
        font = pygame.font.Font(None, 24)
        log_width = screen_width * 2/3
        log_height = screen_height / 8
        log_x = 10
        log_y = screen_height - log_height -60

        combat_log = CombatLog(log_x, log_y, log_width, log_height, font, surface)
        self.bite(
            character, fish, bait, surface, menu_theme, location, screen_width, screen_height, combat_log
        )  # TODO lots of casting logic, this is for testing

    def bite(self, character, fish, bait, surface, menu_theme, location, screen_width, screen_height, combat_log):
        if character.fishing_experience < fish.minimum_fishing_experience:
            self.level_too_low(character, fish, bait, surface, menu_theme, location, screen_width, screen_height, combat_log)
        else:
            if fish.eats == ["all"]:

                battle = Battle(combat_log)
                battle.battle_fish(character, fish, bait, surface, menu_theme, location, screen_width, screen_height)
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

    def level_too_low(self, character, fish, bait, surface, menu_theme, location, screen_width, screen_height, combat_log):
        print(
            "\nYou hooked a big one!"
        )  # creating difficulties here that get passed through the battle functions
        if character.fishing_experience * 2 >= fish.minimum_fishing_experience:
            print("\nIt feels like you have a fair chance to beat this one.")
            self.continue_or_quit(character, fish, bait, surface, menu_theme, location, screen_width, screen_height, combat_log, difficulty="easy")
        elif character.fishing_experience * 3 >= fish.minimum_fishing_experience:
            print("\nIt feels pretty hefty!")
            self.continue_or_quit(character, fish, bait, surface, menu_theme, location, screen_width, screen_height, combat_log, difficulty="medium")
        elif character.fishing_experience * 4 >= fish.minimum_fishing_experience:
            print("\nYou can tell this is gonna be a tough fight.")
            self.continue_or_quit(character, fish, bait, surface, menu_theme, location, screen_width, screen_height, combat_log, difficulty="hard")

        else:
            print(
                "\nThere's no way you're gonna reel this beast in! Quit while you can!"
            )
            self.continue_or_quit(character, fish, bait, surface, menu_theme, location, screen_width, screen_height, combat_log, difficulty="impossible")

    def continue_or_quit(self, character, fish, bait, surface, menu_theme, location, screen_width, screen_height, combat_log, difficulty):

        choice = input(
            "\nPress Enter to fight the fish, or type 'Q' and press Enter to cut the line and give up.\n"
        )
        if choice == "":
            battle = Battle(combat_log)
            battle.battle_fish(character, fish, bait, surface, menu_theme, location, screen_width, screen_height, difficulty)
        elif choice == "Q".lower():
            pass  # TODO cutting line penalty?

    def give_up(self):
        pass
