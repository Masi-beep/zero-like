import pygame

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
TITLE = "zero like"
FRAMERATE = 60

from scripts.sprites import Sprite
from scripts.player import Player


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True     

        # grops
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.enemy_srpites = pygame.sprite.Group()

        # random block
        block_surf = pygame.Surface((WINDOW_WIDTH, 150))
        block_surf.fill("white")
        self.block = Sprite((0, WINDOW_HEIGHT - 75), block_surf, (self.all_sprites, self.collision_sprites))
        
        block_surf_2 = pygame.Surface((150, 450))
        block_surf_2.fill("white")
        self.block_2 = Sprite((WINDOW_WIDTH - 300, 100 ), block_surf_2, (self.all_sprites, self.collision_sprites))

        block_surf_3 = pygame.Surface((150, WINDOW_HEIGHT))
        block_surf_3.fill("white")
        self.block_3 = Sprite((WINDOW_WIDTH - 10, 0), block_surf_3, (self.all_sprites, self.collision_sprites))
        
        block_surf_4 = pygame.Surface((450, 100))
        block_surf_4.fill("white")
        self.block_4 = Sprite((300, WINDOW_HEIGHT - 350), block_surf_4, (self.all_sprites, self.collision_sprites))
        
        self.player = Player((WINDOW_WIDTH/2, WINDOW_HEIGHT/2), self.all_sprites, self.collision_sprites)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self, dt):
        self.all_sprites.update(dt)

    def render(self):
        self.display_surface.fill("black")
        self.all_sprites.draw(self.display_surface)

    def run(self): 
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000
            # events 
            self.handle_events() 
            # update
            self.update(dt)
            # render
            self.render()

            pygame.display.update() 
        pygame.quit()

if __name__ == "__main__":
    Game().run()

