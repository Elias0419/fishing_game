import pygame
import pygame_menu

clock, screen_width, screen_height, surface, menu_theme, font, global_log = None, None, None, None, None, None, None

def init():
    global clock, screen_width, screen_height, surface, menu_theme, font, global_log

    pygame.init()

    clock = pygame.time.Clock()
    info_object = pygame.display.Info()
    screen_width, screen_height = info_object.current_w, info_object.current_h

    surface = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Fishing RPG")

    menu_theme = pygame_menu.themes.THEME_DARK.copy()
    menu_theme.title_offset = (5, -2)
    menu_theme.widget_font_size = 25
    menu_theme.menu_width = int(screen_width * 0.9)
    menu_theme.menu_height = int(screen_height * 0.9)
    pygame.font.init()
    font = pygame.font.Font(None, 24)

def get_globals():
    # debug_info = f"""
    # clock: {clock!r} (Type: {type(clock).__name__})
    # screen_width: {screen_width!r} (Type: {type(screen_width).__name__})
    # screen_height: {screen_height!r} (Type: {type(screen_height).__name__})
    # surface: {surface!r} (Type: {type(surface).__name__})
    # menu_theme: {menu_theme!r} (Type: {type(menu_theme).__name__})
    # font: {font!r} (Type: {type(font).__name__})
    # global_log: {global_log!r} (Type: {type(global_log).__name__})
    # """
    #
    # print(debug_info)
    return clock, screen_width, screen_height, surface, menu_theme, font, global_log
