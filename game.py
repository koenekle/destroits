#!/usr/bin/python
# -*- coding: <utf-8> -*-
import sys

from pygame.locals import QUIT, KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT, KEYUP

from entities import *


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = self.__init_screen()
        self.player = Player(250, 250)
        self.players = pygame.sprite.RenderPlain(self.player)
        self.destroits = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.clock = pygame.time.Clock()

    def __init_screen(self) -> pygame.Surface:
        screen = pygame.display.set_mode(GAMESIZE)
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
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    self.player.set_acceleration(0, -0.5)
                elif event.key == K_DOWN:
                    self.player.set_acceleration(0, 0.5)
                elif event.key == K_LEFT:
                    self.player.set_acceleration(-0.5, 0)
                elif event.key == K_RIGHT:
                    self.player.set_acceleration(0.5, 0)
            elif event.type == KEYUP:
                if event.key == K_UP:
                    self.player.set_acceleration(0, 0.5)
                elif event.key == K_DOWN:
                    self.player.set_acceleration(0, -0.5)
                elif event.key == K_LEFT:
                    self.player.set_acceleration(0.5, 0)
                elif event.key == K_RIGHT:
                    self.player.set_acceleration(-0.5, 0)

    def render(self) -> None:
        self.screen.blit(self.background, (0, 0))
        self.players.draw(self.screen)
        self.destroits.draw(self.screen)
        self.bullets.draw(self.screen)
        pygame.display.flip()

    def update(self) -> None:
        self.spawn_destroits()
        self.players.update()
        self.destroits.update()
        self.bullets.update()

    def spawn_destroits(self) -> None:
        if random() < Asteroid.SPAWN_CHANCE:
            self.destroits.add(Asteroid())
