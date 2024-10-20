import pygame
import pygame_menu
from util import (
    LoopController,
    LoopControllerManager,
    Popup,
    create_popup,
    run_popup,
    load_image,
)
from conf import get_globals
from locations import Location, World, StreamInTheWoods
from character import Character, Player

from battle import Cast
from state_manager import StateManager

state_manager = StateManager()

clock, screen_width, screen_height, surface, menu_theme, font, global_log, manager = (
    get_globals()
)

CELL_SIZE = 100


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


flag = False  # DEBUG REMOVE ME
flag2 = False  # DEBUG REMOVE ME


def check_location(player, locations, character):
    global flag, flag2
    player_pos = player.position
    for location in locations:
        # print(location.recently_entered)
        if (
            location.occupies(player_pos[0], player_pos[1])
            and not location.recently_entered
        ):
            location.recently_entered = True
            do_you_want_to_enter_location(character, location)

            if not flag:  # DEBUG REMOVE ME
                print("entered", location.name)
                flag = True
                flag2 = False
            # print(f"Entered location: {location.name}")
            break
        elif (
            not location.occupies(player_pos[0], player_pos[1])
            and location.recently_entered
        ):
            location.recently_entered = False

            if not flag2:  # DEBUG REMOVE ME
                print("exited", location.name)
                flag2 = True
                flag = False


def do_you_want_to_enter_location(character, location):
    location_text = f"{location.name} test"
    buttons = [
        ("Enter", lambda: go_fishing(character, location)),
        ("Decline", lambda: decline_location(character, location)),
    ]

    popup = Popup(manager, location_text, buttons)
    loop_controller = LoopControllerManager.get_controller(
        "do_you_want_to_enter_location"
    )
    loop_controller.active = True
    while loop_controller.active:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if popup:
                popup.handle_event(event)
            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(surface)

        pygame.display.update()


def decline_location(character, location):
    print("decline")  # TODO


def choose_location(character):
    grid = Grid(CELL_SIZE, 100)  # 100x100 grid, total size 10,000x10,000
    player = Player(character, grid, (50, 50))
    viewport = Viewport(screen_width, screen_height)
    map_image = load_image("images/grid_map.png", grid.width, grid.height)
    all_sprites = pygame.sprite.Group(player)
    world = World.get_instance(character)
    locations = world.locations
    loop_controller = LoopControllerManager.get_controller("choose_location")
    loop_controller.active = True
    while loop_controller.active:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys_pressed = pygame.key.get_pressed()
        player.update(keys_pressed)
        viewport.center_on(player, grid)

        surface.blit(map_image, (0, 0), viewport.rect)

        for sprite in all_sprites:
            new_topleft = (
                sprite.grid.to_pixel(sprite.position[0], sprite.position[1])[0]
                - viewport.rect.left,
                sprite.grid.to_pixel(sprite.position[0], sprite.position[1])[1]
                - viewport.rect.top,
            )
            if sprite.rect.topleft != new_topleft:
                # print(f"Player moved to {new_topleft} on screen.")
                sprite.rect.topleft = new_topleft
            surface.blit(sprite.image, sprite.rect)

        pygame.display.flip()
        clock.tick(30)
        check_location(player, locations, character)
        pygame.display.update()


def go_fishing(character, location):
    # print("go_fishing", character, location)
    location.recently_entered = True
    fish = location.get_fish()
    bait = character.gear[0]["bait"]
    cast = Cast(character, fish, bait, location)
    set_loop_controllers()
    cast.cast_line()


def set_loop_controllers():
    choose_location_loop = LoopControllerManager.get_controller("choose_location")
    choose_location_loop.active = False
    do_you_want_to_enter_location_loop = LoopControllerManager.get_controller(
        "do_you_want_to_enter_location"
    )
    do_you_want_to_enter_location_loop.active = False


class Viewport:
    def __init__(self, width, height):
        self.rect = pygame.Rect(0, 0, width, height)

    def center_on(self, player, grid):
        self.rect.centerx = player.rect.centerx
        self.rect.centery = player.rect.centery

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > grid.width:
            self.rect.right = grid.width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > grid.height:
            self.rect.bottom = grid.height


class Grid:
    def __init__(self, cell_size, num_cells):
        self.cell_size = cell_size
        self.num_cells = num_cells
        self.width = num_cells * cell_size
        self.height = num_cells * cell_size

    def to_pixel(self, grid_x, grid_y):
        return grid_x * self.cell_size, grid_y * self.cell_size
