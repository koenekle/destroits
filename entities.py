import math
from random import random
from typing import Tuple, List

import numpy as np
from pygame.surface import Surface

import resourceloader
import util
from config import *
from util import Vector2D


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
        x, y = pos
        self.rect.x = round(x)
        self.rect.y = round(y)

    @property
    def speed(self) -> Vector2D:
        return self.__speed

    @speed.setter
    def speed(self, speed: Vector2D) -> None:
        # Max speed check
        if np.linalg.norm(speed) > self.MAX_SPEED:
            normed_speed = speed / np.linalg.norm(speed)
            speed = normed_speed * self.MAX_SPEED
        self.__speed = speed
        self.rotate_img()

    def move(self) -> None:
        if not np.all(self.acceleration == np.zeros((2, 1))):
            self.speed += self.acceleration
        self.pos = np.add(self.pos, self.speed)
        self.check_for_walkout()


    def rotate_img(self):
        x, y = self.speed / np.linalg.norm(self.pos)
        self.image = pygame.transform.rotate(self.orig_image, math.atan2(-y, x) * 180 / math.pi)

    def check_for_walkout(self) -> None:
        for axis in (0, 1):
            if 0 > self.pos[axis] or self.pos[axis] > GAMESIZE[axis]:
                self.pos[axis] = self.pos[axis] % GAMESIZE[axis]

    def update(self) -> None:
        self.move()


class Player(Entity):
    MAX_SPEED = 5.0
    KEY_MAPPING = KEY_MAPPING

    def __init__(self, pos: Vector2D) -> None:
        self.image_still = resourceloader.get_image_scaled("spaceship", (48, 24))
        self.animation = Animation(10,
            resourceloader.get_image_scaled("spaceship_move_0", (48, 24)),
                                   resourceloader.get_image_scaled("spaceship_move_1", (48, 24)))
        image = self.image_still
        self.rotation = 0
        super().__init__(pos, image=image)
        self.mouse_position = np.array((0, 0))
        self.reload_counter = 0
        self.accelerating = False

    def update(self) -> None:
        if not self.accelerating:
            self.animation.reset()
            self.image = self.image_still
            self.orig_image = self.image.copy()
        else:
            self.image = self.animation.update()
            self.orig_image = self.image.copy()
        self.rotate_img()
        self.move()
        self.accelerating = False

    def rotate_img(self):
        self.image = pygame.transform.rotate(self.orig_image, -self.rotation)

    @property
    def direction(self) -> Vector2D:
        return util.rotate(np.array((1.0, 0.0)), self.rotation)

    @direction.setter
    def direction(self, dir: Vector2D) -> None:
        x, y = dir[0], dir[1]
        self.rotation = math.atan2(-y, x) * 180 / math.pi

    def turn_left(self) -> None:
        self.rotation -= TURN_SPEED
        self.rotate_img()

    def turn_right(self) -> None:
        self.rotation += TURN_SPEED
        self.rotate_img()

    def accelerate(self) -> None:
        self.speed += util.rotate(ACCELERATION_DELTA, self.rotation)
        self.accelerating = True

    def can_shoot(self) -> bool:
        if self.reload_counter == 0:
            self.reload_counter = RELOAD_TIME
            return True
        else:
            self.reload_counter += -1
            return False


class Asteroid(Entity):
    MAX_SPEED = 5.0
    MIN_SIZE = 20
    MAX_SIZE = 50
    MIN_DISTANCE_PLAYER = 16

    SPAWN_CHANCE = DESTROIT_SPAWN_CHANCE

    def __init__(self, player_pos: Vector2D = None, pos: Vector2D = None, move_direction: Vector2D = None,
                 size=None) -> None:
        if size is None:
            self.__size = round(random() * (self.MAX_SIZE - self.MIN_SIZE) + self.MIN_SIZE)
        else:
            self.__size = round(size)
        image = resourceloader.get_image_scaled("destroit", (self.__size, self.__size))
        if pos is None:
            pos = self.calc_spawn_pos(player_pos)
        super().__init__(pos, size=np.ones((2, 1)) * self.__size, image=image)
        if move_direction is not None:
            self.speed = move_direction
        elif player_pos is not None:
            self.speed = self.calc_move_direction(player_pos)
        else:
            Exception("Need to provide either player_pos or move_direction")

    def set_acceleration(self, dX: float, dY: float) -> None:
        self.acceleration = self.acceleration + np.array((dX, dY))

    def calc_spawn_pos(self, player_pos: Vector2D) -> Vector2D:
        distance_player = self.MIN_DISTANCE_PLAYER - 1
        while self.MIN_DISTANCE_PLAYER > distance_player:
            pos = np.array((random() * GAMESIZE.x, random() * GAMESIZE.y))
            distance_player = np.linalg.norm(pos - player_pos)
        return pos

    def calc_move_direction(self, player_pos: Vector2D) -> Vector2D:
        rel_pos = (player_pos - self.pos)
        return rel_pos / np.linalg.norm(rel_pos) * self.MAX_SPEED * random()

    def kill(self):
        new_size = self.__size / 2
        if new_size > self.MIN_SIZE:
            a1 = Asteroid(pos=np.copy(self.pos), move_direction=util.rotate(self.speed, -10), size=new_size)
            a2 = Asteroid(pos=np.copy(self.pos), move_direction=util.rotate(self.speed, 10), size=new_size)
            a1.add(self.groups())
            a2.add(self.groups())
        super(Asteroid, self).kill()


class Bullet(Entity):
    MAX_SPEED = 5.0
    SIZE = (10, 2)

    def __init__(self, pos: Vector2D, direction: Vector2D) -> None:
        image = resourceloader.get_image("bullet")
        super().__init__(pos, size=Bullet.SIZE, image=image)
        self.speed = Bullet.MAX_SPEED * np.array(direction)

    def check_for_walkout(self) -> None:
        for axis in (0, 1):
            if 0 > self.pos[axis] or self.pos[axis] > GAMESIZE[axis]:
                self.kill()


class Animation:
    def __init__(self, frame_length: int, *images: List[Surface]):
        self.images = images
        self.index = 0
        self.frame_length = frame_length
        self.frame_time = 0

    def reset(self) -> None:
        self.index = 0

    def update(self) -> Surface:
        if self.frame_time == round(self.frame_length / len(self.images)):
            self.frame_time = 0
            self.index += 1
        else:
            self.frame_time += 1
        if self.index >= len(self.images):
            self.index = 0
        return self.images[self.index]

    def get_image(self, index: int) -> Surface:
        return self.images[index]
