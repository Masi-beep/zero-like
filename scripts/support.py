import pygame
import os

BASE_IMG_PATH = "assets/images"
BASE_SND_PATH = "assets/sounds"


def move_toward(current, target, max_delta):
    if abs(target - current) <= max_delta:
        return target
    return current + max_delta * (1 if target > current else -1)


