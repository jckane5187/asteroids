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