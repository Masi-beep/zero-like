import pygame

from scripts.sprites import PhysicsSprite

enemy_surf = pygame.Surface((30,40))
enemy_surf.fill("gold")

ENEMY_ANIMATIONS = {
    "idle": [enemy_surf],
}


class Enemy(PhysicsSprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(pos, 300, ENEMY_ANIMATIONS, groups, collision_sprites)
    
    def die(self):
        self.kill()
