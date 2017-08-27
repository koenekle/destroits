#!/usr/bin/python
# -*- coding: <utf-8> -*-
import numpy as np
import pygame
import sys
from pygame.locals import QUIT

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (50, 50, 50)


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = self.__init_screen()
        self.player = Player(250, 250)
        self.group = pygame.sprite.RenderPlain(self.player)
        self.clock = pygame.time.Clock()

    def __init_screen(self):
        screen = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("DESTROITS")

        # Fill background
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill(BLACK)
        self.background = background

        # Blit everything to the screen
        screen.blit(background, (0, 0))
        pygame.display.flip()

        return screen

    def start(self) -> None:
        # Event loop
        while True:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
            self.draw()

    def draw(self):
        print("Drawing")

        self.screen.blit(self.background, (0, 0))
        self.group.draw(self.screen)
        pygame.display.flip()


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
