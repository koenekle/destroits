#!/usr/bin/python
# -*- coding: <utf-8> -*-

from Game import Game


def launch() -> None:
    cur_game = Game()
    cur_game.start()


if __name__ == '__main__':
    launch()
