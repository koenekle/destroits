import os
from os import listdir
from os.path import isfile, join

import pygame

IMAGE_PATH = "./resource/img"
images_dict = dict()

images = [ f for f in listdir(IMAGE_PATH) if isfile(join(IMAGE_PATH,f)) and f.endswith('png') ]
for filename in images:
    images_dict[os.path.splitext(filename)[0]] = pygame.image.load(join(IMAGE_PATH,filename))

def get_image(name: str) -> pygame.Surface:
    return images_dict[name]