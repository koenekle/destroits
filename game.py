#!/usr/bin/python
# -*- coding: <utf-8> -*-
import sys

import pygame
from pygame.locals import QUIT

from colors import BLACK
from entity import Player


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = self.__init_screen()
        self.player = Player(250, 250)
        self.players = pygame.sprite.RenderPlain(self.player)
        self.destroits = pygame.sprite.Group()
        self.clock = pygame.time.Clock()

    def __init_screen(self) -> pygame.Surface:
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
            self.process_input()
            self.update()
            self.render()

    def process_input(self) -> None:
        for event in pygame.event.get():
            print(event)
            if event.type == QUIT:
                sys.exit(0)
            if event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_UP:
                self.player.update_velocity(0, -1)
            if event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_DOWN:
                self.player.update_velocity(0, 1)
            if event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_LEFT:
                self.player.update_velocity(-1, 0)
            if event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_RIGHT:
                self.player.update_velocity(1, 0)

    def render(self) -> None:
        self.screen.blit(self.background, (0, 0))
        self.players.draw(self.screen)
        pygame.display.flip()

    def update(self) -> None:
        self.players.update()
        self.destroits.update()
