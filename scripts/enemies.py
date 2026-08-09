import pygame

from scripts.sprites import PhysicsSprite

enemy_surf = pygame.Surface((30,40))
enemy_surf.fill("gold")

ENEMY_ANIMATIONS = {
    "idle": [enemy_surf],
}

