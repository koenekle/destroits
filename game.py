#!/usr/bin/python
# -*- coding: <utf-8> -*-
import sys

from pygame.locals import QUIT, KEYDOWN, KEYUP, MOUSEMOTION

from entities import *


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = self.__init_screen()
        self.player = Player((250.0, 250.0))
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
        pygame.display.flip()

    def update(self) -> None:
        self.players.update()
        self.destroits.update()
        self.bullets.update()

        collisions = pygame.sprite.groupcollide(self.bullets, self.destroits, True, False)

        self.spawn_destroits()

        if self.player.can_shoot():
            rel_pos = (self.player.mouse_position - self.player.pos).astype(np.float64)
            direction = (rel_pos / np.linalg.norm(rel_pos)).astype(np.float64)
            bullet = Bullet(self.player.pos, direction)
            self.bullets.add(bullet)


    def spawn_destroits(self) -> None:
        if random() < Asteroid.SPAWN_CHANCE:
            self.destroits.add(Asteroid())
