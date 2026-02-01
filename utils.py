import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, TITLE_FONT, MENU_FONT

def position_wrap(x, y):
    if x < 0:
        x = SCREEN_WIDTH
    if x > SCREEN_WIDTH:
        x = 0
    if y > SCREEN_HEIGHT:
        y = 0
    if y < 0:
        y = SCREEN_HEIGHT
    return x, y

def kill_offscreen(x, y, obj):
    if x < 0 or x > SCREEN_WIDTH or y > SCREEN_HEIGHT or y < 0:
        obj.kill()
        return True
    return False

def set_game_state(new_state, player, score, asteroids, shots, ui_elements_dict=None):
    if ui_elements_dict is not None:
        ui_elements_dict.clear()

    if new_state == "MENU":
        ui_elements_dict["title_surface"] = TITLE_FONT.render("ASTEROIDS", True, "white")
        ui_elements_dict["title_rect"] = ui_elements_dict["title_surface"].get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))

        ui_elements_dict["menu_play"] = MENU_FONT.render("PLAY", True, "white")
        ui_elements_dict["menu_play_rect"] = ui_elements_dict["menu_play"].get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

        ui_elements_dict["menu_quit"] = MENU_FONT.render("QUIT", True, "white")
        ui_elements_dict["menu_quit_rect"] = ui_elements_dict["menu_quit"].get_rect(centerx=(SCREEN_WIDTH / 2))
        ui_elements_dict["menu_quit_rect"].top = ui_elements_dict["menu_play_rect"].bottom + 36

        for roid in asteroids:
            roid.kill()
        shots.empty()
        player = None
        score = None

    elif new_state == "PLAYING":
        for roid in asteroids:
            roid.kill()
        shots.empty()
        

    elif new_state == "GAME_OVER":
        ui_elements_dict["title_surface"] = TITLE_FONT.render("GAME OVER", True, "white")
        ui_elements_dict["title_rect"] = ui_elements_dict["title_surface"].get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))

        ui_elements_dict["menu_play"] = MENU_FONT.render("PLAY", True, "white")
        ui_elements_dict["menu_play_rect"] = ui_elements_dict["menu_play"].get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

        ui_elements_dict["menu_quit"] = MENU_FONT.render("QUIT", True, "white")
        ui_elements_dict["menu_quit_rect"] = ui_elements_dict["menu_quit"].get_rect(centerx=(SCREEN_WIDTH / 2))
        ui_elements_dict["menu_quit_rect"].top = ui_elements_dict["menu_play_rect"].bottom + 36
    
    else:
        raise Exception(f"Invalid game_state: {new_state}")
    
    if ui_elements_dict is None:
        return new_state, player, score, asteroids, shots
    
    return new_state, player, score, asteroids, shots, ui_elements_dict