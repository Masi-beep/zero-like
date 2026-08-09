import pygame

from os import walk
from os.path import join

BASE_IMG_PATH = "assets/images"
BASE_SND_PATH = "assets/sounds"


def move_toward(current, target, max_delta):
    if abs(target - current) <= max_delta:
        return target
    return current + max_delta * (1 if target > current else -1)

def import_image(*path, format='png', alpha=True):
    full_path = join(BASE_IMG_PATH, *path) + f".{format}"
    surf = pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()
    return surf

def import_folder(*path, alpha=True):
    frames = []
    for folder_path, _, file_names in walk(join(BASE_IMG_PATH, *path)): 
        for file_name in sorted(file_names, key = lambda name: int(name.split(".")[0])):
            full_path = join(folder_path, file_name)
            surf = pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()
            frames.append(surf)
    return frames
# for player frames use "run": import_folder("player", "run")
