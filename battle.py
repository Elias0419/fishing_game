import random
import math
from state_manager import StateManager, WorldState, CharacterState, BattleState
from util import LoopController, LoopControllerManager, get_level_from_experience
# from world_map import choose_location
from locations import World
import pygame
import pygame_menu
from collections import deque
from functools import wraps
from contextlib import redirect_stdout
import io
from textwrap import wrap
import sys

import time

from conf import get_globals

clock, screen_width, screen_height, surface, menu_theme, font, global_log = get_globals()

POPUP_EVENT = pygame.USEREVENT + 1
popup_queue = deque()


################################################################
################################################################
import pprint
import inspect

def debug_print(*args):
    pp = pprint.PrettyPrinter(indent=4)
    frame = inspect.currentframe()
    try:
        caller = inspect.getouterframes(frame)[1]
        frameinfo = inspect.getframeinfo(caller[0])
        args_name = inspect.getargvalues(caller[0]).locals
        arg_names = frameinfo.code_context[0].strip().split("debug_print(")[1].split(")")[0].replace(" ", "").split(",")

        for arg_name, obj in zip(arg_names, args):
            print(f"\n\nName: {arg_name}")
            print("Type:", type(obj))
            print("Value:")
            pp.pprint(obj)
            print("-" * 40, "\n\n")
    finally:
        del frame
################################################################
################################################################

# class LoopController:
#     def __init__(self, controller_id):
#         self.active = True
#         self.id = controller_id

# class LoopControllerManager:
#     _instances = {}
#
#     @classmethod
#     def get_controller(cls, controller_id):
#         if controller_id not in cls._instances:
#             cls._instances[controller_id] = LoopController(controller_id)
#         return cls._instances[controller_id]
#
#     @classmethod
#     def end_specific_loop(cls, controller_id):
#         if controller_id in cls._instances:
#             cls._instances[controller_id].active = False

######
# popup
def render_and_blit(surface, font, text, pos):
    text_surf = font.render(text, True, (255, 255, 255))
    surface.blit(text_surf, pos)

def create_popup(text, buttons=None):

    width, height = 300, 200
    x, y = (screen_width - width) // 2, (screen_height - height) // 2

    popup_surface = pygame.Surface((width, height))
    popup_surface.fill(getattr(menu_theme, 'background_color', (100, 100, 100)))

    text_surface = font.render(text, True, getattr(menu_theme, 'text_color', (255, 255, 255)))
    text_rect = text_surface.get_rect(center=(width // 2, height // 3))

    button_objects = []
    if buttons:
        button_width, button_height = 80, 30
        spacing = (width - len(buttons) * button_width) // (len(buttons) + 1)
        for index, (label, callback) in enumerate(buttons):
            button_x = spacing + index * (button_width + spacing)
            button_y = height - button_height - 20
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            button_text = font.render(label, True, getattr(menu_theme, 'button_text_color', (0, 0, 0)))
            button_objects.append({'rect': button_rect, 'text': button_text, 'callback': callback})

    return {
        'surface': popup_surface,
        'text_surface': text_surface,
        'text_rect': text_rect,
        'buttons': button_objects,
        'x': x,
        'y': y
    }

should_close_popup = False

def close_popup():
    global should_close_popup
    should_close_popup = True

def run_popup(popup):
    global should_close_popup
    running = True
    popup['should_close'] = False

    while running:
        if should_close_popup:
            popup['should_close'] = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for button in popup['buttons']:
                    if button['rect'].collidepoint(mouse_pos[0] - popup['x'], mouse_pos[1] - popup['y']):
                        button['callback']()
                        if popup['should_close']:
                            running = False

        surface.blit(popup['surface'], (popup['x'], popup['y']))
        surface.blit(popup['text_surface'], popup['text_rect'].topleft)
        for button in popup['buttons']:
            pygame.draw.rect(surface, getattr(menu_theme, 'button_color', (200, 200, 200)), button['rect'].move(popup['x'], popup['y']))
            surface.blit(button['text'], button['rect'].move(popup['x'], popup['y']).topleft) # FIXME text missing
        pygame.display.update()
        clock.tick(30)

def check_popup_interaction(popup, event):

    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        for button in popup['buttons']:
            if button['rect'].collidepoint(x, y):
                button['callback']()

######

class CharacterStatusBox:
    def __init__(self, character):
        self.character = character
        self.width = screen_width * 1/7
        self.height = screen_height / 7
        self.x = 10
        self.y = 100
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):

        surface.fill((0, 0, 0), self.rect)
        character_name = self.character.name
        stamina_text = f"Stamina: {self.character.stamina}/{self.character.max_stamina}"
        reel_name, reel_max_drag, reel_current_drag = self.get_reel_details()
        reel_drag_text = f"Drag: {reel_current_drag}/{reel_current_drag}"
        render_and_blit(surface, font, character_name, (self.x + 10, self.y + 10))
        # TEST +15 for now
        render_and_blit(surface, font, stamina_text, (self.x + 10, self.y + 25))
        render_and_blit(surface, font, reel_name, (self.x + 10, self.y + 40))
        render_and_blit(surface, font, reel_drag_text, (self.x + 10, self.y + 55))

    def get_reel_details(self):
        reel = self.character.gear[0]["rod"].reel
        reel_name = reel.name
        reel_max_drag = reel.max_drag
        reel_current_drag = reel.drag_lbs
        return reel_name, reel_max_drag, reel_current_drag



class FishStatusBox:
    def __init__(self, fish):
        self.fish = fish
        self.width = screen_width * 1/7
        self.height = screen_height / 7
        self.x = 350
        self.y = 100
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):

        surface.fill((0, 0, 0), self.rect)
        fish_name, fish_stamina_string = self.get_fish_details()
        render_and_blit(surface, font, fish_name, (self.x + 10, self.y + 10))
        render_and_blit(surface, font, fish_stamina_string, (self.x + 10, self.y + 25))

    def get_fish_details(self): # TODO
        # experience can unlock things like - being able to see stamina details, fish name, weight, etc
        # otherwise we give generic statements like "the fish feels heavy", etc
        # for example
        # if character.experience_skills.fish_identification_level >= fish.minimum_identification_level:
        #     fish_name = fish.name
        # else:
        #     fish_name = "???"
        # we can also do stuff like
        # if character.experience_skills.{fish.name}.has_been_identified: # (for example, caught 100 of them and now can identify by feel)
        #    pass
        # or
        # if character.experience_skills.fish_weight_estimation < 10:
        #   fish_weight = "That's a heavy one!"
        # elif character.experience_skills.fish_weight_estimation >10 and <90:
        #     fish_weight = "Feels like about {fish_weight} * {some_random_innaccuracy}"
        # elif character.experience_skills.fish_weight_estimation >=90:
        #     fish_weight = fish.weight

        """
        TEST
        For development we'll just show these details
        """
        fish_name = self.fish.name
        fish_stamina_string = f"{self.fish.stamina}/{self.fish.max_stamina}"

        return fish_name, fish_stamina_string



class CombatLog: # Lazy init?
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CombatLog, cls).__new__(cls)
        return cls._instance

    def __init__(self, x, y, log_width, log_height):
        if not hasattr(self, "_init"):

            self.rect = pygame.Rect(x, y, log_width, log_height)

            self.messages = []
            self.visible_messages = self.rect.height // 20
            self.combat_log_start_index = 0
            self._init = True



    def add_message(self, message):
        lines = message.split('\n')
        self.messages.extend(lines)
        self.combat_log_start_index = max(0, len(self.messages) - self.visible_messages)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            try:
                if event.button == 4:  # Scroll up
                    self.combat_log_start_index = max(0, self.combat_log_start_index - 1)
                elif event.button == 5:  # Scroll down
                    self.combat_log_start_index = min(len(self.messages) - self.visible_messages, self.combat_log_start_index + 1)
            except IndexError as e:
                pass

    def draw(self):

        surface.fill((0, 0, 0), self.rect)
        start_y = self.rect.bottom - 20
        end_index = min(self.combat_log_start_index + self.visible_messages, len(self.messages))

        for i in range(self.combat_log_start_index, end_index):
            try:
                text_surf = font.render(self.messages[i], True, (255, 255, 255))
                surface.blit(text_surf, (self.rect.x + 5, start_y))
                start_y -= 20
            except IndexError as e:
                pass







def init_global_log(log_x, log_y, log_width, log_height):
    global global_log
    global_log = CombatLog(log_x, log_y, log_width, log_height)

def get_global_log():
    global global_log
    if global_log is None:
        log_width = screen_width * 2/3
        log_height = screen_height / 8
        log_x = 10
        log_y = screen_height - log_height -60
        init_global_log(log_x, log_y, log_width, log_height)

    return global_log

class LogDecorator:
    def __init__(self, log):
        self.log_func = log
        self.log = None

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self.log is None:
                self.log = self.log_func

            str_buffer = io.StringIO()
            with redirect_stdout(str_buffer):
                result = func(*args, **kwargs)
            output = str_buffer.getvalue()
            if output:
                self.log.add_message(output.strip())
            return result
        return wrapper


@LogDecorator(log=get_global_log())
def add_popup(message, duration=2000, x=320, y=240, font='Arial', font_size=36, font_style=None, to_combat_log=False):
    if font_style:
        font = pygame.font.SysFont(font, font_size, bold='bold' in font_style, italic='italic' in font_style)
    else:
        font = pygame.font.SysFont(font, font_size)

    popup_queue.append((message, pygame.time.get_ticks(), duration, x, y, font))
    if to_combat_log:
        print(message)

def show_popups():
    current_time = pygame.time.get_ticks()
    if popup_queue:
        message, start_time, duration, x, y, font = popup_queue[0]
        if current_time - start_time > duration:
            popup_queue.popleft()
        else:
            text = font.render(message, True, (255, 255, 255))
            text_rect = text.get_rect(center=(x, y))
            surface.blit(text, text_rect)







class Battle:
    def __init__(self, character, fish, location):
        self.drag_too_high_count = 0
        self.drag_too_low_count = 0
        # self.drag_init_flag = False
        self.max_safe_drag = None
        self.first_round = True
        self.location = location
        self.fish = fish
        self.character = character
        self.character_status_box = CharacterStatusBox(character)
        self.fish_status_box = FishStatusBox(fish)

    def battle_fish(self, bait, difficulty):

        # while True:
            if difficulty == None:
                self.none_battle(difficulty, bait)
                    # break
            elif difficulty == "easy":
                self.easy_battle(difficulty,  bait)
                    # break
            elif difficulty == "medium":
                self.medium_battle(difficulty, bait)
                    # break
            elif difficulty == "hard":
                self.hard_battle(difficulty, bait)
                    # break
            elif difficulty == "impossible":
                self.impossible_battle(difficulty, bait)
                    # break

    def print_battle_menu(self, bait, difficulty):

        fish = self.fish
        pre_battle_fish_stamina = fish.stamina
        menu_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
        menu = pygame_menu.Menu("Battle", screen_width, screen_height, theme=menu_theme)
        # menu.add.button('Reel', reel_fish)
        menu.add.button('Let Fish Take Line', self.let_the_fish_take_line, difficulty, bait, pre_battle_fish_stamina)
        menu.add.button('Adjust Drag', self.adjust_drag)
        # menu.add.button('Other Options', other_options)
        # menu.add.button('Cut Your Line', cut_line)
        menu.add.button('Quit', pygame_menu.events.EXIT)

        loop_controller = LoopControllerManager.get_controller("print_battle_menu")
        loop_controller.active = True

        while loop_controller.active:
            # screen.fill((0, 0, 0))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.reel(difficulty, bait)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:  # Scroll up
                        try:
                            global_log.combat_log_start_index = max(0, global_log.combat_log_start_index - 1)
                        except IndexError:
                            pass
                    elif event.button == 5:  # Scroll down
                        try:
                            global_log.combat_log_start_index = min(len(global_log.messages) - global_log.visible_messages, global_log.combat_log_start_index + 1)

                        except IndexError:
                            pass

            menu.update(events)
            menu.draw(surface)
            global_log.draw()
            self.character_status_box.draw()
            self.fish_status_box.draw()
            show_popups()
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

    @LogDecorator(log=get_global_log())
    def adjust_drag(self):
        add_popup("message")
        # reel = character.gear[0]["rod"].reel
        # reel_name = reel.name
        # reel_max_drag = reel.max_drag
        # reel_current_drag = reel.drag_lbs
        #
        # print(
        #     f"\nThe {reel_name} has a maximum drag of {reel_max_drag} lbs.\nIt's currently set to {reel_current_drag} lbs."
        # )
        #
        # while True:
        #     choice = input(
        #         f"Set the drag by entering a number less than or equal to {reel_max_drag} lbs:\n"
        #     )
        #     if self.check_integer(choice):
        #         choice = int(choice)
        #         if choice > reel_max_drag:
        #             print(f"{reel_name} can only go up to {reel_max_drag} lbs.")
        #         elif choice == reel_current_drag:
        #             print(f"{reel_name} is already set to {choice} lbs.")
        #         else:
        #             adjustment_direction = (
        #                 "up" if choice > reel_current_drag else "down"
        #             )
        #             adjustment = abs(reel_current_drag - choice)
        #             reel.drag_lbs = choice
        #             print(f"{reel_name} set to {reel.drag_lbs} lbs.")
        #             return adjustment, adjustment_direction
        #
        #     else:
        #         print("Please enter a valid number.")

    @LogDecorator(log=get_global_log())
    def calculate_drag(
        self, difficulty, bait, adjustment=0, adjustment_direction=None
    ):
        character = self.character
        fish = self.fish
        reel = character.gear[0]["rod"].reel
        fish_weight = fish.weight_lbs
        line_strength = character.gear[0]["rod"].line.breaking_strength_lbs
        reel_max_drag = reel.max_drag
        reel_current_drag = reel.drag_lbs
        baseline_max_safe_drag = int(min(line_strength, reel_max_drag) * 0.8)

        # print(  # DEBUG remove me
        #     "\nInside calculate_drag\nMax:",
        #     reel_max_drag,
        #     "\nCurrent",
        #     reel_current_drag,
        #     "\nAdjustment",
        #     adjustment,
        #     "\nDirection",
        #     adjustment_direction,
        # )

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
        world = World.get_instance(character)
        # debug_print(character, self, world) # DEBUG
        state_manager.save_state(
            f"{character.character_id}.pkl", character, self, world
        )
        minimum_effective_drag = int(
            max(0.5 * fish_weight, baseline_max_safe_drag * 0.5)
        )  # * difficulty # Character skill here probably

        # print(  # DEBUG remove me
        #     "Minimum effective drag:",
        #     minimum_effective_drag,
        #     "\nMaximum safe drag:",
        #     self.max_safe_drag,
        # )
        if fish_weight > self.max_safe_drag:
            add_popup(
                f"{reel.name} screams under the weight of the fish!\nReduce the drag before something breaks!", to_combat_log=True
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

    @LogDecorator(log=get_global_log())
    def let_the_fish_take_line(
        self, difficulty, bait, pre_battle_fish_stamina
    ):
        print("combat log test")
        character = self.character
        fish = self.fish
        # print("take line")  # TODO maybe certain fish take line differently or stamina loss affects them differently
        if fish.stamina <= pre_battle_fish_stamina * 0.2:
            print("The fish seems too weak to take any line\n")
            self.take_line_stamina_increase(character, fish_low_stamina=True)
        else:  # TODO different fish weights and gear affect how the line is pulled
            # gear damage could be here too
            # needs more complex logic for calculating loss and gain
            percent_loss = random.randint(10, 50)
            fish_stamina_loss = round(fish.stamina * percent_loss / 100)
            print("The fish takes line.")
            print(f"Your {character.gear[0]['rod'].reel.name} squeals under the pressure.")
            fish.stamina -= fish_stamina_loss
            print(f"The fish used {fish_stamina_loss} stamina.")
            self.take_line_stamina_increase(character)

    def take_line_stamina_increase(self, fish_low_stamina=False):
        character = self.character
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

    def easy_battle(self, bait, difficulty):
        # self.print_battle_stamina(character, fish)
        print("\ndrag_too_high easy_battle before", self.drag_too_high_count)
        self.drag_too_high_count = 0
        print("drag_too_high easy_battle after", self.drag_too_high_count)

        self.print_battle_menu(bait, difficulty)
            # return True

    def medium_battle(self, bait, difficulty): # TODO
        self.drag_too_high_count = 0
        print("medium_battle")
        return True

    def hard_battle(self, bait, difficulty): # TODO
        self.drag_too_high_count = 0
        print("hard_battle")
        return True

    def impossible_battle(self, bait, difficulty): # TODO
        self.drag_too_high_count = 0
        print("impossible_battle")
        return True

    def none_battle(self, bait, difficulty): # TODO
        character = self.character
        fish = self.fish
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

    def lose_bait(self, difficulty, bait):
        # TODO more complex bait logic
        # chance = self.random_chance(50)
        # print(chance)
        if self.random_chance(50):
            bait.amount -= 1
            print(f"You lost a {bait.name}\n{bait.amount} remaining")
        else:
            print("\nYou didn't lose your bait this time.\n")

    def reel(self, difficulty, bait):
        self.calculate_drag(difficulty, bait)
        if self.check_win(difficulty, bait):
            return True
        else:
            # self._TESTING_(character)
            if self.calculate_char_stamina_loss(difficulty, bait):
                return True
            elif self.calculate_fish_stamina_loss(difficulty, bait):
                return True

            return False

    def _TESTING_(self, character):  # TODO REMOVE ME
        character.stamina = 100

    def calculate_char_stamina_loss(self, difficulty, bait):
        character = self.character
        fish = self.fish
        rounded_fish_weight = math.ceil(fish.weight_lbs)
        experience_gap = fish.minimum_fishing_experience - character.fishing_experience
        char_stamina_loss = rounded_fish_weight + random.randint(
            int(experience_gap / 4), experience_gap
        )
        character.stamina -= char_stamina_loss
        print(f"You used {char_stamina_loss} stamina!")

    def calculate_fish_stamina_loss(
        self, difficulty, bait, weight="normal"
    ):
        character = self.character
        fish = self.fish
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
            self.end_battle(difficulty, bait)
            # print(f"The fish has exhausted all its stamina and the battle ends.")
            return True
        else:
            fish.stamina -= stamina_loss
            print(
                f"The fish used {stamina_loss} stamina!"
            )  # TODO figure out what to do with fractional stamina
            return False

    def check_win(self, difficulty, bait):
        character = self.character
        fish = self.fish
        if difficulty == None:
            if self.random_chance(90):  # TEST
                self.end_battle(difficulty, bait)

                return True
            else:
                # print("doh")  # TODO
                return False
        elif difficulty == "easy": # More difficulties
            if self.random_chance(1):  # TEST
                self.end_battle(difficulty, bait)
                return True
            else:
                return False

    def end_battle(self, difficulty, bait):
        self.drag_init_flag = False
        self.drag_too_high_count = 0
        self.drag_too_low_count = 0
        character = self.character
        fish = self.fish
        exp = fish.gives_exp
        # character.fishing_experience += exp # TODO testing
        print("exp increase disabled for testing")
        old_age = character.age
        new_age = get_level_from_experience(character.fishing_experience)
        if new_age != old_age:
            print("age increased")
        state_manager = StateManager()
        world = World.get_instance(character)
        state_manager.save_state(
            f"{character.character_id}.pkl", character, self, world
        )  # dummy world state
        self.print_battle_summary(difficulty, bait, exp)

    def print_battle_summary(self, difficulty, bait, exp):


        buttons = [
            ("Cast again", lambda: self.cast_again()),
            ("Back to World Map", lambda: self.back_to_world_map())
            ]



        messages = """
            f"You caught a {fish.name}!",
            f"Difficulty: {difficulty}",
            f"Length: {fish.length_inch:.2f} inches",
            f"Weight: {fish.weight_lbs:.2f} pounds",
            f"You gained {exp} fishing experience!"
        """

        popup = create_popup(messages, buttons)
        run_popup(popup)


    def back_to_world_map(self):
        from world_map import choose_location
        print("click")
        loop_controller = LoopControllerManager.get_controller("print_battle_menu")
        loop_controller.active = False
        print(LoopControllerManager.print_all_loop_instances()) # DEBUG
        choose_location(self.character)

    def cast_again(self):
        character = self.character
        location = self.location
        fish = location.get_fish()
        bait = character.gear[0]["bait"]
        cast = Cast(character, fish, bait, location)
        cast.cast_line()

    def random_chance(self, percent):
        return random.random() < percent / 100


class Cast:
    def __init__(self, character, fish, bait, location):
        self.get_log()
        self.character = character
        # self.character_box_test() # REMOVE ME

        self.fish = fish
        self.bait = bait


        self.location = location

    # def character_box_test(self): # REMOVE ME
    #     CharacterStatusBox(self.character)


    def get_log(self):
        # font = pygame.font.Font(None, 24)
        log_width = screen_width * 2/3
        log_height = screen_height / 8
        log_x = 10
        log_y = screen_height - log_height -60
        init_global_log(log_x, log_y, log_width, log_height)


    def cast_line(self):
        # combat_log = CombatLog(log_x, log_y, log_width, log_height, font, surface)
        # init_global_log(log_x, log_y, log_width, log_height, font, self.surface) # Going to need to fix this someday, maybe
        self.bite()  # TODO lots of casting logic, this is for testing

    def bite(self):
        if self.character.fishing_experience < self.fish.minimum_fishing_experience:
            self.level_too_low()
        else:
            if self.fish.eats == ["all"]:

                battle = Battle(self.character, self.fish, self.location)
                battle.battle_fish(self.bait)
            elif self.bait.name in self.fish.eats:
                battle = Battle(self.character, self.fish, self.location)
                battle.battle_fish(self.bait) # TODO
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

    def level_too_low(self):
        # Example using both combat log and popup)
        add_popup("\nYou hooked a big one!", to_combat_log=True)
        # creating difficulties here that get passed through the battle functions
        if self.character.fishing_experience * 2 >= self.fish.minimum_fishing_experience:
            print("\nIt feels like you have a fair chance to beat this one.")
            self.continue_or_quit(difficulty="easy")
        elif self.character.fishing_experience * 3 >= self.fish.minimum_fishing_experience:
            print("\nIt feels pretty hefty!")
            self.continue_or_quit(difficulty="medium")
        elif self.character.fishing_experience * 4 >= self.fish.minimum_fishing_experience:
            print("\nYou can tell this is gonna be a tough fight.")
            self.continue_or_quit(difficulty="hard")

        else:
            print(
                "\nThere's no way you're gonna reel this beast in! Quit while you can!"
            )
            self.continue_or_quit(difficulty="impossible")

    def continue_or_quit(self, difficulty):
        # TODO probably only do this on hard+

        menu = pygame_menu.Menu("", screen_width, screen_height, theme=menu_theme)
        menu.add.label(f"The fish is {difficulty}")
        # name_entry = menu.add.text_input("", default="")
        menu.add.button('Continue', self.continue_game, difficulty)
        menu.add.button('Cut the line', pygame_menu.events.BACK)

        loop_controller = LoopControllerManager.get_controller("continue_or_quit")
        loop_controller.active = True
        while loop_controller.active:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()

            if menu.is_enabled():
                menu.update(events)
                menu.draw(surface)

            pygame.display.update()

    def continue_game(self, difficulty):
            # character, fish, bait, surface, menu_theme, location, screen_width, screen_height, combat_log, difficulty = args
            #         print(f""" # DEBUG REMOVE ME
            # Character: {character}
            # Fish: {fish}
            # Bait: {bait}
            # Surface: {surface}
            # Menu Theme: {menu_theme}
            # Location: {location}
            # Screen Width: {screen_width}
            # Screen Height: {screen_height}
            # Combat Log: {combat_log}
            # Difficulty: {difficulty}
            # """)
        loop_controller = LoopControllerManager.get_controller("continue_or_quit")
        loop_controller.active = False
        battle = Battle(self.character, self.fish, self.location)
        battle.battle_fish(self.bait, difficulty)

        # choice = input(
        #     "\nPress Enter to fight the fish, or type 'Q' and press Enter to cut the line and give up.\n"
        # )
        # if choice == "":
        #     battle = Battle(combat_log)
        #     battle.battle_fish(character, fish, bait, surface, menu_theme, location, screen_width, screen_height, difficulty)
        # elif choice == "Q".lower():
        #     pass  # TODO cutting line penalty?

    def give_up(self):
        pass
