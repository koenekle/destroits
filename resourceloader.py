import os
from os import listdir
from os.path import isfile, join

import pygame

import config

IMAGE_PATH = config.IMAGE_PATH
images_dict = dict()


def init_resource_loader():
    images = [f for f in listdir(IMAGE_PATH) if isfile(join(IMAGE_PATH, f)) and f.endswith('png')]
    for filename in images:
        images_dict[os.path.splitext(filename)[0]] = load_png(join(IMAGE_PATH, filename))


def get_image(name: str) -> pygame.Surface:
    if name in images_dict:
        return images_dict[name]
    images_dict[name] = load_png(join(IMAGE_PATH, name))
    return images_dict[name]

def get_image_scaled(name:str, size: tuple):
    return pygame.transform.scale(get_image(name), size)



def load_png(path):
    """ Load image and return image object"""
    try:
        image = pygame.image.load(path)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as message:
        print('Cannot load image:', path)
        raise SystemExit(message)
    return image
