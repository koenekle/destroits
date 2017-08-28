from collections import namedtuple

import pygame
from pygame.constants import K_w, K_s, K_d, K_a

Point = namedtuple("Point", ("x", "y"))

DEBUG = False
pygame.font.init()
DBG_FONT = pygame.font.SysFont(None, 14)

FPS = 60

BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GREY = (50, 50, 50)
WHITE = (255, 255, 255)

GAMESIZE = Point(1000, 1000)

ACCELERATION_DELTA = 0.5
KEY_MAPPING = {
        K_w: (0, -ACCELERATION_DELTA),
        K_s: (0, ACCELERATION_DELTA),
        K_d: (ACCELERATION_DELTA, 0),
        K_a: (-ACCELERATION_DELTA, 0)}
RELOAD_TIME = 20

