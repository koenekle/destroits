import numpy as np
import pygame


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
        self.velocity = np.array((0, 0))

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
    VELO_MAX = (10, 10)
    VELO_MIN = (0, 0)

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.image = pygame.Surface([50, 50])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos = (x, y)

    def update(self):
        pass