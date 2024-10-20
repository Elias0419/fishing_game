import pickle
import os
import random

import pygame
import pygame_menu
import pygame_gui


# from locations import Location, World, StreamInTheWoods
from state_manager import WorldState, LocationState, StateManager

# from battle import Cast, LoopController, LoopControllerManager
# from world_map import Grid, Viewport, CELL_SIZE
# from character import Character, Player

from conf import get_globals

clock, screen_width, screen_height, surface, menu_theme, font, global_log, manager = (
    get_globals()
)


class LoopController:
    def __init__(self, controller_id):
        self.active = True
        self.id = controller_id


class LoopControllerManager:
    _instances = {}

    @classmethod
    def get_controller(cls, controller_id):
        if controller_id not in cls._instances:
            cls._instances[controller_id] = LoopController(controller_id)
        return cls._instances[controller_id]

    @classmethod
    def end_specific_loop(cls, controller_id):
        if controller_id in cls._instances:
            cls._instances[controller_id].active = False

    @classmethod  # DEBUG
    def print_all_loop_instances(cls):
        for i, instance in enumerate(cls._instances):
            print(i, instance, cls._instances[instance].active)


import pygame
import pygame_gui

class Popup:
    def __init__(
        self,
        manager,
        text,
        buttons,
        position=None,
        text_area_size=None,
        button_size=(80, 30),
        size=(300, 200),
        label_position = None,
        style=None,
        debug=False,
    ):
        if position is None:
            x = (screen_width - size[0]) // 2
            y = (screen_height - size[1]) // 2
            position = (x, y)

        if style is None:
            style = {}
        window_style = style.get("window", {})
        label_style = style.get("label", {})
        button_style = style.get("button", {})



        self.window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect(position, size),
            manager=manager,
            window_display_title="",
            resizable=False,
            **window_style,
        )

        if text_area_size is None:
            text_area_size = (size[0] - 20, size[1] - 100)
        if label_position is None:
            label_position = (10, 10)

        label_rect = pygame.Rect(label_position, text_area_size)


        self.text = pygame_gui.elements.UILabel(
            relative_rect=label_rect,
            text=text,
            manager=manager,
            container=self.window,
            **label_style,
        )

        self.buttons = []
        button_width, button_height = button_size
        button_y = size[1] - button_height - 25
        spacing = (size[0] - len(buttons) * button_width) // (len(buttons) + 1)

        for index, (label, callback) in enumerate(buttons):
            button_x = spacing + index * (button_width + spacing)
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((button_x, button_y), button_size),
                text=label,
                manager=manager,
                container=self.window,
                **button_style,
            )
            self.buttons.append((button, callback))


    def handle_event(self, event):
        for button, callback in self.buttons:
            if (
                event.type == pygame_gui.UI_BUTTON_PRESSED
                and event.ui_element == button
            ):
                callback()
                self.window.kill()


def get_level_from_experience(experience):
    level_map = create_level_map()
    for level in sorted(level_map.keys(), reverse=True):
        if experience >= level_map[level]:
            return level
    return 10


def create_level_map():  # FIXME
    return {x: 100 * 2 ** (x - 10) for x in range(10, 101)}


def create_popup(text, buttons=None):

    width, height = 300, 200
    x, y = (screen_width - width) // 2, (screen_height - height) // 2

    popup_surface = pygame.Surface((width, height))
    popup_surface.fill(getattr(menu_theme, "background_color", (100, 100, 100)))

    text_surface = font.render(
        text, True, getattr(menu_theme, "text_color", (255, 255, 255))
    )
    text_rect = text_surface.get_rect(center=(width // 2, height // 3))

    button_objects = []
    if buttons:
        button_width, button_height = 80, 30
        spacing = (width - len(buttons) * button_width) // (len(buttons) + 1)
        for index, (label, callback) in enumerate(buttons):
            button_x = spacing + index * (button_width + spacing)
            button_y = height - button_height - 20
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            button_text = font.render(
                label, True, getattr(menu_theme, "button_text_color", (0, 0, 0))
            )
            button_objects.append(
                {"rect": button_rect, "text": button_text, "callback": callback}
            )

    return {
        "surface": popup_surface,
        "text_surface": text_surface,
        "text_rect": text_rect,
        "buttons": button_objects,
        "x": x,
        "y": y,
    }


should_close_popup = False


def close_popup():
    global should_close_popup
    should_close_popup = True


def run_popup(popup):
    global should_close_popup
    running = True
    popup["should_close"] = False

    while running:
        if should_close_popup:
            popup["should_close"] = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for button in popup["buttons"]:
                    if button["rect"].collidepoint(
                        mouse_pos[0] - popup["x"], mouse_pos[1] - popup["y"]
                    ):
                        button["callback"]()
                        if popup["should_close"]:
                            running = False

        surface.blit(popup["surface"], (popup["x"], popup["y"]))
        surface.blit(popup["text_surface"], popup["text_rect"].topleft)
        for button in popup["buttons"]:
            pygame.draw.rect(
                surface,
                getattr(menu_theme, "button_color", (200, 200, 200)),
                button["rect"].move(popup["x"], popup["y"]),
            )
            surface.blit(
                button["text"], button["rect"].move(popup["x"], popup["y"]).topleft
            )  # FIXME text missing
        pygame.display.update()
        clock.tick(30)


def check_popup_interaction(popup, event):

    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        for button in popup["buttons"]:
            if button["rect"].collidepoint(x, y):
                button["callback"]()


def log_output(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        update_log(result)
        return result

    return wrapper


def load_image(path, width, height):
    image = pygame.image.load(path)
    return image


def create_log_surface(width, height):
    log_surface = pygame.Surface((width, height))
    return log_surface


def update_log(message, log_surface, font, color=(255, 255, 255)):
    text = font.render(message, True, color)


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
    from rods import Twig, TenLbMono, Reel
    from bait import Worm

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


# def test(character):  # unlocking locations
#     world = World.get_instance(character)
#     battle = ""
#     for location in world.locations:
#         if location.name == "Stream in the Woods":
#             location.unlocked = True
#             break
#     StateManager.save_state(f"{character.character_id}.pkl", character, battle, world)


# def available_locations(character):
#     player_level = character.age
#     world = World.get_instance(character)
#     _, _, world_state = StateManager.load_state(f"{character.character_id}.pkl")
#     if world_state.locations != []:
#         StateManager.apply_state(world_state, world)
#     return [
#         loc
#         for loc in world.locations
#         if player_level >= loc.minimum_level and loc.unlocked
#     ]
#
# flag = False # DEBUG REMOVE ME
# flag2 = False # DEBUG REMOVE ME
# def check_location(player, locations, character):
#     global flag, flag2
#     player_pos = player.position
#     for location in locations:
#         # print(location.recently_entered)
#         if location.occupies(player_pos[0], player_pos[1]) and not location.recently_entered:
#             location.recently_entered = True
#             do_you_want_to_enter_location(character, location)
#
#             if not flag: # DEBUG REMOVE ME
#                 print("entered", location.name)
#                 flag = True
#                 flag2 = False
#             # print(f"Entered location: {location.name}")
#             break
#         elif not location.occupies(player_pos[0], player_pos[1]) and location.recently_entered:
#             location.recently_entered = False
#
#             if not flag2: # DEBUG REMOVE ME
#                 print("exited", location.name)
#                 flag2 = True
#                 flag = False
#
# def do_you_want_to_enter_location(character, location):
#     location_text = f"{location.name} test"
#     # popup_width, popup_height = int(screen_width / 3), int(screen_height / 3)
#     buttons = [
#     ("Enter", lambda: go_fishing(character, location)),
#     ("Decline", lambda: decline_location(character, location))
#     ]
#     popup = create_popup(location_text, buttons)
#     run_popup(popup)
#     # # print(popup_width, popup_height)
#     # popup_surface = pygame.Surface(popup_width, popup_height)
#     # while True:
#     #     events = pygame.event.get()
#     #     for event in events:
#     #         if event.type == pygame.QUIT:
#     #             pygame.quit()
#     #             exit()
#     #     popup_surface.blit(location_text)
#     #     surface.blit(popup_surface)
#
#     # go_fishing(character, location)
#
# def decline_location(character, location):
#     print("decline") # TODO
#
# def choose_location(character):
#     grid = Grid(CELL_SIZE, 100)  # 100x100 grid, total size 10,000x10,000
#     player = Player(character, grid, (50, 50))
#     viewport = Viewport(screen_width, screen_height)
#     map_image = load_image('images/grid_map.png', grid.width, grid.height)
#     all_sprites = pygame.sprite.Group(player)
#     world = World.get_instance(character)
#     locations = world.locations
#     loop_controller = LoopControllerManager.get_controller("choose_location")
#
#     while loop_controller.active:
#         events = pygame.event.get()
#         for event in events:
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 exit()
#
#         keys_pressed = pygame.key.get_pressed()
#         player.update(keys_pressed)
#         viewport.center_on(player, grid)
#
#         surface.blit(map_image, (0, 0), viewport.rect)
#
#         for sprite in all_sprites:
#             new_topleft = (sprite.grid.to_pixel(sprite.position[0], sprite.position[1])[0] - viewport.rect.left,
#                            sprite.grid.to_pixel(sprite.position[0], sprite.position[1])[1] - viewport.rect.top)
#             if sprite.rect.topleft != new_topleft:
#                 # print(f"Player moved to {new_topleft} on screen.")
#                 sprite.rect.topleft = new_topleft
#             surface.blit(sprite.image, sprite.rect)
#
#         pygame.display.flip()
#         clock.tick(20)
#         check_location(player, locations, character)  # Check for location changes
#
#         pygame.display.update()

# def choose_location(character):
#     menu = pygame_menu.Menu("World Map", screen_width, screen_height, theme=menu_theme)
#     available = available_locations(character)
#     for i, location in enumerate(available, 1):
#         menu.add.button(
#             f"{i}. {location.name}",
#             go_fishing,
#             character,
#             location,
#         )
#
#     while True:
#         events = pygame.event.get()
#         for event in events:
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 exit()
#
#         if menu.is_enabled():
#             menu.update(events)
#             menu.draw(surface)
#         pygame.display.update()


# def display_stats(character):
#     print(
#         f"\nName {character.name}\nAge {character.age}\nExperience {character.fishing_experience}\nStrength {character.strength}\nStamina {character.stamina}"
#     )
#
#
# def display_equipment(character):
#     print(
#         f"\nRod:\n{character.gear[0]['rod'].name}\nHit Points: {character.gear[0]['rod'].hit_points}\nBreaking Strength (lbs): {character.gear[0]['rod'].breaking_strength_lbs}\n\nLine:\n{character.gear[0]['rod'].line.name}\n\nReel:\n{character.gear[0]['rod'].reel.name}\nMax Drag: {character.gear[0]['rod'].reel.drag_lbs}"
#     )


# def go_fishing(character, location):
#     location.recently_entered = True
#
#     # location = choose_location(character, surface, menu_theme)
#     fish = location.get_fish()
#     bait = character.gear[0]["bait"]
#     cast = Cast(character, fish, bait, location)
#     loop_controller = LoopControllerManager.get_controller("choose_location")
#     loop_controller.active = False
#     cast.cast_line()
