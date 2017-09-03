import math
from math import fabs, copysign
from random import random
from typing import Tuple

from pygame.locals import KEYUP

import resourceloader
from config import *


class Entity(pygame.sprite.Sprite):
    """
    Base Class for all Entities

    self.image and self.rect should be overwritten
    """
    MAX_SPEED = 5.0

    def __init__(self, pos: Vector2D, size=(10, 10), color=GREY, image=None) -> None:
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
    def pos(self) -> Vector2D:
        return self.real_pos

    @pos.setter
    def pos(self, pos: Vector2D) -> None:
        self.real_pos = pos
        self.rect.x = round(pos[0])
        self.rect.y = round(pos[1])

    def move(self) -> None:
        self.speed += self.acceleration
        # Max speed check
        if fabs(self.speed[0]) > self.MAX_SPEED:
            self.speed = np.array((copysign(self.MAX_SPEED, self.speed[0]), self.speed[1]))
        if fabs(self.speed[1]) > self.MAX_SPEED:
            self.speed = np.array((self.speed[0], copysign(self.MAX_SPEED, self.speed[1])))
        self.pos = self.pos + self.speed
        self.check_for_walkout()

        x, y = self.speed / np.linalg.norm(self.pos)
        self.image = pygame.transform.rotate(self.orig_image, math.atan2(-y, x) * 180 / math.pi)

    def check_for_walkout(self) -> None:
        for axis in (0, 1):
            if 0 > self.pos[axis] or self.pos[axis] > GAMESIZE[axis]:
                self.pos[axis] = self.pos[axis] % GAMESIZE[axis]


    def update(self) -> None:
        raise NotImplementedError("abstract Method")


class Player(Entity):
    MAX_SPEED = 5.0
    KEY_MAPPING = KEY_MAPPING

    def __init__(self, pos: Vector2D) -> None:
        image = resourceloader.get_image("player")
        super().__init__(pos, image=image)
        self.mouse_position = np.array((0, 0))
        self.reload_counter = 0


    def update(self) -> None:
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
    MAX_SPEED = 5.0
    MIN_SIZE = 10
    MAX_SIZE = 30
    MIN_DISTANCE_PLAYER = 16

    SPAWN_CHANCE = DESTROIT_SPAWN_CHANCE

    def __init__(self, player_pos: Vector2D) -> None:
        image = pygame.image.load("resource/img/destroit.png")
        super().__init__(self.calc_spawn_pos(player_pos),
                         size=np.ones((2, 1)) * (random() * (self.MAX_SIZE - self.MIN_SIZE) + self.MIN_SIZE),
                         image=image)
        self.speed = self.calc_move_direction(player_pos)


    def update(self) -> None:
        self.move()

    def set_acceleration(self, dX: float, dY: float) -> None:
        self.acceleration = self.acceleration + np.array((dX, dY))

    def calc_spawn_pos(self, player_pos: Vector2D) -> Vector2D:
        distance_player = self.MIN_DISTANCE_PLAYER - 1
        while self.MIN_DISTANCE_PLAYER > distance_player:
            pos = np.array((random() * GAMESIZE.x, random() * GAMESIZE.y))
            distance_player = np.linalg.norm(pos-player_pos)
        return pos

    def calc_move_direction(self, player_pos: Vector2D) -> Vector2D:
        rel_pos = (player_pos - self.pos)
        return rel_pos / np.linalg.norm(rel_pos) * self.MAX_SPEED * random()



class Bullet(Entity):
    MAX_SPEED = 5.0
    SIZE = (10, 2)

    def __init__(self, pos: Vector2D,
                 direction: Vector2D) -> None:
        image = pygame.image.load("resource/img/bullet.png")
        super().__init__(pos, size=Bullet.SIZE, image=image)
        self.speed = Bullet.MAX_SPEED * np.array(direction)

    def update(self) -> None:
        self.move()

    def check_for_walkout(self) -> None:
        for axis in (0, 1):
            if 0 > self.pos[axis] or self.pos[axis] > GAMESIZE[axis]:
                self.kill()
