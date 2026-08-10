import pygame

from pytmx.util_pygame import load_pygame
from os.path import join

from scripts.settings import * 
from scripts.level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True     
        
        self.tmx_maps = {0: load_pygame(join("data","levels","test.tmx"))}
        
        self.current_stage = Level(self.tmx_maps[0])

    def run(self): 
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000
            # events 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            # update
            self.current_stage.run(dt)

            pygame.display.update() 
        pygame.quit()

if __name__ == "__main__":
    Game().run()

