import math
from math import fabs, copysign
from random import random
from typing import Tuple

import numpy as np
from pygame.locals import KEYUP

from config import *


class Entity(pygame.sprite.Sprite):
    """
    Base Class for all Entities

    self.image and self.rect should be overwritten
    """

    def __init__(self, pos: np.ndarray(dtype=np.float64, shape=(2, 1)), size=(10, 10), color=GREY, image=None) -> None:
        super().__init__()
        if size is not None:
            if not image:
                self.image = pygame.Surface(size)
                self.image.fill(color)
            else:
                self.image = image
            self.orig_image = self.image.copy()
            self.rect = self.image.get_rect()
        assert type(pos) is np.ndarray
        self.pos = pos
        self.acceleration: Tuple[float, float] = np.array((0.0, 0.0))
        self.speed: Tuple[float, float] = np.array((0.0, 0.0))

    @property
    def pos(self) -> np.array:
        return self.real_pos

    @pos.setter
    def pos(self, pos: np.array):
        self.real_pos = pos
        self.rect.x = round(pos[0])
        self.rect.y = round(pos[1])

    def move(self):
        self.speed += self.acceleration
        # Max speed check
        if fabs(self.speed[0]) > self.MAX_SPEED[0]:
            self.speed = np.array((copysign(self.MAX_SPEED[0], self.speed[0]), self.speed[1]))
        if fabs(self.speed[1]) > self.MAX_SPEED[1]:
            self.speed = np.array((self.speed[0], copysign(self.MAX_SPEED[1], self.speed[1])))
        self.pos = self.pos + self.speed
        self.check_for_walkout()

        x, y = self.speed / np.linalg.norm(self.pos)
        self.image = pygame.transform.rotate(self.orig_image, math.atan2(-y, x) * 180 / math.pi)

    def check_for_walkout(self):
        for axis in (0, 1):
            if 0 > self.pos[axis] or self.pos[axis] > GAMESIZE[axis]:
                self.pos[axis] = self.pos[axis] % GAMESIZE[axis]


    def update(self) -> None:
        raise NotImplementedError("abstract Method")


class Player(Entity):
    MAX_SPEED = (5, 5)
    KEY_MAPPING = KEY_MAPPING

    def __init__(self, pos: np.ndarray(dtype=np.float64, shape=(2, 1))) -> None:
        image = pygame.image.load("resource/img/player.png")
        super().__init__(pos, image=image)
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
            self.reload_counter = RELOAD_TIME
            return True
        else:
            self.reload_counter += -1
            return False


class Asteroid(Entity):
    MAX_SPEED = (5, 5)
    MIN_SIZE = 10
    MAX_SIZE = 20

    SPAWN_CHANCE = 0.01

    def __init__(self) -> None:
        image = pygame.image.load("resource/img/destroit.png")
        super().__init__(np.array((random() * GAMESIZE.x, random() * GAMESIZE.y)),
                         size=np.ones((2, 1)) * (random() * (self.MAX_SIZE - self.MIN_SIZE) + self.MIN_SIZE),
                         image=image)

    def update(self):
        self.move()

    def set_acceleration(self, dX: float, dY: float) -> None:
        self.acceleration = self.acceleration + np.array((dX, dY))


class Bullet(Entity):
    MAX_SPEED = (5.0, 5.0)
    SIZE = (10, 2)

    def __init__(self, pos: np.ndarray(dtype=np.float64, shape=(2, 1)),
                 direction: np.ndarray(dtype=np.float64, shape=(2, 1))) -> None:
        image = pygame.image.load("resource/img/bullet.png")
        super().__init__(pos, size=Bullet.SIZE, image=image)
        self.speed = Bullet.MAX_SPEED * np.array(direction)

    def update(self):
        self.move()

    def check_for_walkout(self):
        for axis in (0, 1):
            if 0 > self.pos[axis] or self.pos[axis] > GAMESIZE[axis]:
                self.kill()
