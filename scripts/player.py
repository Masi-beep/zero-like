import pygame

from scripts.sprites import PhysicsSprite

idle_surf = pygame.Surface((30, 40))
idle_surf.fill("red")
run_surf = pygame.Surface((30,40))
run_surf.fill("yellow")
jump_surf = pygame.Surface((30,40))
jump_surf.fill("blue")
dash_surf = pygame.Surface((30,40))
dash_surf.fill("green")
wall_slide_surf = pygame.Surface((30,40))
wall_slide_surf.fill("purple")

PLAYER_ANIMATIONS = {
    "idle": [idle_surf],
    "run": [run_surf],
    "jump": [jump_surf],
    "dash": [dash_surf],
    "wall_slide": [wall_slide_surf],
}

class Player(PhysicsSprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(pos, 530, PLAYER_ANIMATIONS, groups, collision_sprites) 

    def input(self):
        keys = pygame.key.get_pressed()
        just_pressed = pygame.key.get_just_pressed()

        if just_pressed[pygame.K_UP]:
            self.jump()

        if just_pressed[pygame.K_x] and self.control_lock_timer <= 0:
            self.dash()

        if just_pressed[pygame.K_z]:
            self.attack()

        if self.control_lock_timer <= 0:
            self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])

    def jump(self):
        if self.on_floor:
            self.direction.y = -12
            self.on_floor = False 
            return True
        if self.on_wall_left:
            self.direction.y = -12
            self.direction.x = 1
            self.velocity_x = self.max_speed
            self.control_lock_timer = 0.30  
            return True
        if self.on_wall_right:
            self.direction.y = -12
            self.direction.x = -1
            self.velocity_x = -self.max_speed
            self.control_lock_timer = 0.30
            return True
    
    def dash(self):
        if self.dash_timer <= 0:
            self.direction.y = 0 
            self.dash_timer = 0.15
            self.control_lock_timer = 0.30
            return True
    
    def attack(self):
        print("whoosh")

    def update(self, dt):
        self.control_lock_timer = max(0, self.control_lock_timer - dt)
        self.input()
        super().update(dt)

        # animation state
        if self.on_wall_left or self.on_wall_right:
            self.set_action("wall_slide")
        elif not self.on_floor:
            self.set_action("jump")
        elif self.dash_timer > 0:
            self.set_action("dash")
        elif self.direction.x != 0:
            self.set_action("run")
        else:
            self.set_action("idle")

       
