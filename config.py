from collections import namedtuple

import pygame
from pygame.constants import K_w, K_d, K_a

Point = namedtuple("Point", ("x", "y"))


DEBUG = False
pygame.font.init()
DBG_FONT = pygame.font.SysFont(None, 14)
GAME_FONT = pygame.font.SysFont(None, 20)
IMAGE_PATH = "./resource/img"

FPS = 60

BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GREY = (50, 50, 50)
WHITE = (255, 255, 255)

GAMESIZE = Point(700, 700)

ACCELERATION_DELTA = (0.2, 0.0)
TURN_SPEED = 4
CAN_SHOOT_ANYWHERE = False

KEY_MAPPING = {
    K_w: "accelerate",
    K_d: "turn_right",
    K_a: "turn_left"}
RELOAD_TIME = 15

DESTROIT_SPAWN_CHANCE = 0.01
DESTROIT_POINT_SCALE_FACTOR = 20.0

