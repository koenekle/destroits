from math import fabs, copysign
from random import random
from typing import Tuple

import numpy as np
import pygame
from pygame.locals import QUIT, KEYDOWN, K_w, K_s, K_a, K_d, KEYUP

import config
from config import *


class Entity(pygame.sprite.Sprite):
    """
    Base Class for all Entities

    self.image and self.rect should be overwritten
    """

    def __init__(self, pos: np.ndarray(dtype=np.float64, shape=(2, 1)), size=(10, 10), color=GREY) -> None:
        super().__init__()
        if size is not None:
            self.image = pygame.Surface(size)
            self.image.fill(color)
            self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.acceleration: Tuple[float, float] = np.array((0.0, 0.0))
        self.speed: Tuple[float, float] = np.array((0.0, 0.0))

    @property
    def pos(self) -> np.array:
        return np.array((self.rect.x, self.rect.y))

    @pos.setter
    def pos(self, pos: np.array):
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def move(self):
        self.speed += self.acceleration
        # Max speed check
        if fabs(self.speed[0]) > self.MAX_SPEED[0]:
            self.speed = np.array((copysign(self.MAX_SPEED[0], self.speed[0]), self.speed[1]))
        if fabs(self.speed[1]) > self.MAX_SPEED[1]:
            self.speed = np.array((self.speed[0], copysign(self.MAX_SPEED[1], self.speed[1])))
        self.pos = self.pos + self.speed
        x, y = self.pos
        if 0 > x or x > GAMESIZE[0]:
            x = x % GAMESIZE[0]
        if 0 > y or y > GAMESIZE[1]:
            y = y % GAMESIZE[1]
        self.pos = np.array((x, y))

    def update(self) -> None:
        raise NotImplementedError("abstract Method")


class Player(Entity):
    MAX_SPEED = (5, 5)
    KEY_MAPPING = config.KEY_MAPPING
    def __init__(self, pos: np.ndarray(dtype=np.float64, shape=(2, 1))) -> None:
        super().__init__(pos, size=(30, 30), color=RED)
        self.mouse_position = np.array((0, 0))
        self.reload_counter = 0

    def update(self):
        self.move()

    def move_direction(self, type: int, key: int) -> None:
        if type == KEYUP:
            delta = np.negative(Player.KEY_MAPPING[key])
        else:
            delta = Player.KEY_MAPPING[key]
        self.acceleration = self.acceleration + np.array(delta)

    def can_shoot(self) -> bool:
        if self.reload_counter == 0:
            self.reload_counter = config.RELOAD_TIME
            return True
        else:
            self.reload_counter += -1
            return False


class Asteroid(Entity):
    MAX_SPEED = (5, 5)
    MIN_SIZE = 5
    MAX_SIZE = 10

    SPAWN_CHANCE = 0.01

    def __init__(self) -> None:
        super().__init__((random() * GAMESIZE.x, random() * GAMESIZE.y),
                         size=np.ones((2, 1)) * (random() * (self.MAX_SIZE - self.MIN_SIZE) + self.MIN_SIZE),
                         color=BLUE)

    def update(self):
        self.move()

    def set_acceleration(self, dX: float, dY: float) -> None:
        self.acceleration = self.acceleration + np.array((dX, dY))


class Bullet(Entity):
    MAX_SPEED = (5.0, 5.0)
    SIZE = (3, 3)

    def __init__(self, pos: np.ndarray(dtype=np.float64, shape=(2, 1)), direction: np.ndarray(dtype=np.float64, shape=(2, 1))) -> None:
        super().__init__(pos, size=Bullet.SIZE, color=GREEN)
        self.speed = Bullet.MAX_SPEED * np.array(direction)

    def update(self):
        self.move()
