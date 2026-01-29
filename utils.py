import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

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