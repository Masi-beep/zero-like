import pygame

from scripts.sprites import PhysicsSprite


class Player(PhysicsSprite):
    def __init__(self, pos, animations, groups, collision_sprites):
        super().__init__(pos, 530, animations, groups, collision_sprites) 

    def input(self):
        keys = pygame.key.get_pressed()
        just_pressed = pygame.key.get_just_pressed()
        
        if self.control_lock_timer <= 0:
            self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        
        if just_pressed[pygame.K_UP]:
            self.jump()

        if just_pressed[pygame.K_x]:
            self.dash()

    def jump(self):
        if self.on_floor:
            self.direction.y = -15
            self.on_floor = False
            print(f"on_floor={self.on_floor}, on_wall_left={self.on_wall_left}, on_wall_right={self.on_wall_right}") 
            return True
        if self.on_wall_left:
            self.direction.y = -12
            self.direction.x = 1
            self.velocity_x = self.max_speed
            self.control_lock_timer = 0.25
            print(f"on_floor={self.on_floor}, on_wall_left={self.on_wall_left}, on_wall_right={self.on_wall_right}")
            return True
        if self.on_wall_right:
            self.direction.y = -12
            self.direction.x = -1
            self.velocity_x = -self.max_speed
            self.control_lock_timer = 0.25
            print(f"on_floor={self.on_floor}, on_wall_left={self.on_wall_left}, on_wall_right={self.on_wall_right}")
            return True
    
    def dash(self):
        if self.dash_timer <= 0:
            self.direction.y = 0 
            self.dash_timer = 0.25
            self.control_lock_timer = 0.25
            return True

    def update(self, dt):
        self.control_lock_timer = max(0, self.control_lock_timer - dt)
        self.input()
        super().update(dt)
        
