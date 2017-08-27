#!/usr/bin/python
# -*- coding: <utf-8> -*-
import sys

import pygame
from pygame.locals import QUIT

from entity import Player


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
