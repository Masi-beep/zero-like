import pygame

from scripts.settings import *
from scripts.sprites import Sprite
from scripts.player import Player


class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()
        
        # grops
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        self.setup(tmx_map)

    def setup(self, tmx_map):
        for x, y, surf in tmx_map.get_layer_by_name("terrain").tiles():
            Sprite((x*TILE_SIZE,y*TILE_SIZE), surf, (self.all_sprites, self.collision_sprites))
        
        Player((100, 300), self.all_sprites, self.collision_sprites)
                
    def run(self, dt):
        self.all_sprites.update(dt)
        self.display_surface.fill("black")
        self.all_sprites.draw(self.display_surface)
