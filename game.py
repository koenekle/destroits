#!/usr/bin/python
# -*- coding: <utf-8> -*-
import itertools
import sys

from pygame.locals import MOUSEMOTION, KEYDOWN, QUIT
from pygame import Surface

from entities import *


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = self.__init_screen()
        resourceloader.init_resource_loader()
        self.player = Player(np.array((250.0, 250.0)))
        self.players = pygame.sprite.RenderPlain(self.player)
        self.destroits = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.clock = pygame.time.Clock()

    def __init_screen(self) -> Surface:
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
            self.clock.tick(FPS)
            self.process_input()
            self.update()
            self.render()

    def process_input(self) -> None:
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYUP or event.type == KEYDOWN:
                if event.key in self.player.KEY_MAPPING:
                    self.player.move_direction(event.type, event.key)
            elif event.type == MOUSEMOTION:
                self.player.mouse_position = np.array(event.pos)

    def render(self) -> None:
        self.screen.blit(self.background, (0, 0))
        self.players.draw(self.screen)
        self.destroits.draw(self.screen)
        self.bullets.draw(self.screen)

        if DEBUG:
            for sprite in itertools.chain(self.players.sprites(), self.destroits.sprites(), self.bullets.sprites()):
                textsurface = DBG_FONT.render(np.array2string(sprite.pos, precision=0), False, WHITE)
                self.screen.blit(textsurface, (sprite.pos))
        pygame.display.flip()

    def update(self) -> None:
        self.players.update()
        self.destroits.update()
        self.bullets.update()

        collisions = pygame.sprite.groupcollide(self.bullets, self.destroits, True, True)

        self.spawn_destroits()

        if self.player.can_shoot():
            rel_pos = (self.player.mouse_position - self.player.pos)
            direction = (rel_pos / np.linalg.norm(rel_pos))
            bullet = Bullet(self.player.pos, direction)
            self.bullets.add(bullet)

    def spawn_destroits(self) -> None:
        if random() < Asteroid.SPAWN_CHANCE:
            self.destroits.add(Asteroid(self.player.pos))
