import numpy as np
import pygame
from math import fabs, copysign

from colors import RED, GREY


class Entity(pygame.sprite.Sprite):
    """
    Base Class for all Entities

    self.image and self.rect should be overwritten
    """

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.acceleration = np.array((0, 0))

    @property
    def pos(self) -> np.array:
        return np.array((self.rect.x, self.rect.y))

    @pos.setter
    def pos(self, pos: np.array):
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self) -> None:
        raise NotImplementedError("abstract Method")


class Player(Entity):
    MAX_SPEED = (5, 5)

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.image = pygame.Surface([50, 50])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos = (x, y)
        self.acceleration = np.array((0, 0))
        self.speed = np.array((0, 0))

    def update(self):
        self.speed += self.acceleration
        # Max acceleration check
        if fabs(self.speed[0]) > self.MAX_SPEED[0]:
            self.speed = np.array((copysign(self.MAX_SPEED[0], self.speed[0]), self.speed[1]))
        if fabs(self.speed[1]) > self.MAX_SPEED[1]:
            self.speed = np.array((self.speed[0], copysign(self.MAX_SPEED[1], self.speed[1])))
        self.pos = self.pos + self.speed

    def set_acceleration(self, dX: int, dY: int) -> None:
        self.acceleration = self.acceleration + np.array((dX, dY))
