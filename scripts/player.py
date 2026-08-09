import pygame

from scripts.support import move_toward
from scripts.sprites import AnimatedSprite
from scripts.timer import Timer

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
    "idle": {"frames": [idle_surf], "speed": 6},
    "run": {"frames": [run_surf], "speed": 10},
    "jump": {"frames": [jump_surf], "speed": 1},
    "dash": {"frames": [dash_surf], "speed": 3},
    "wall_slide": {"frames": [wall_slide_surf], "speed": 1},
}

class Player(AnimatedSprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(pos, PLAYER_ANIMATIONS, groups)
        
        # movement & collision
        self.collision_sprites = collision_sprites 
        self.gravity = 48 
        self.direction = pygame.Vector2()
        self.on_floor = False

        self.max_speed = 530
        self.velocity_x = 0
        self.floor_accel = 3000
        self.air_accel = 1500
        
        # timers
        self.x_move_timer = Timer(1000)
        self.dash_duration = Timer(200)
        self.dash_cooldown = Timer(400)
        self.attack_cooldown = Timer(500)

    def input(self):
        keys = pygame.key.get_pressed()
        just_pressed = pygame.key.get_just_pressed()

        if keys[pygame.K_UP]:
            self.jump()

        if just_pressed[pygame.K_x] and not self.dash_duration.active:
            self.dash()

        if keys[pygame.K_z] and not self.attack_cooldown.active:
            self.attack()

        if not self.x_move_timer.active and not self.dash_duration.active:
            self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
            
    def move(self, dt):
        if self.dash_duration.active:
            self.direction.x = -1 if self.flip else 1
            self.direction.y *= 0.50
            self.velocity_x = self.direction.x * (self.max_speed * 1.7)
            self.rect.x += self.velocity_x * dt
        else:
            accel = self.floor_accel if self.on_floor else self.air_accel
            target_velocity = self.direction.x * self.max_speed
            self.velocity_x = move_toward(self.velocity_x, target_velocity, accel * dt)

            if self.velocity_x > 0: self.flip = False
            if self.velocity_x < 0: self.flip = True 
            
            self.rect.x += self.velocity_x * dt
        
        self.on_wall_left = False
        self.on_wall_right = False
        self.collision("horizontal")
        
        # vertical velocity
        self.on_floor = False
        self.direction.y += self.gravity * dt
        self.direction.y = min(self.direction.y, 500) # terminal velocity
        self.rect.y += self.direction.y
        self.collision("vertical")

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == "horizontal":
                    self.direction.y *= 0.8
                    if self.velocity_x > 0: 
                        self.rect.right = sprite.rect.left
                        self.on_wall_right = True
                    if self.velocity_x < 0: 
                        self.rect.left = sprite.rect.right
                        self.on_wall_left = True

                elif direction == "vertical":
                    if self.direction.y > 0: self.rect.bottom = sprite.rect.top
                    self.on_floor = True
                    if self.direction.y < 0: self.rect.top = sprite.rect.bottom
                    self.direction.y = 0
    
    def jump(self):
        if self.on_floor:
            self.direction.y = -12
            self.on_floor = False 
            return True
        if self.on_wall_left:
            self.direction.y = -12
            self.direction.x = 1
            self.velocity_x = self.max_speed
            self.x_move_timer.activate()
            return True
        if self.on_wall_right:
            self.direction.y = -12
            self.direction.x = -1
            self.velocity_x = -self.max_speed
            self.x_move_timer.activate()
            return True
    
    def dash(self):
        if not self.dash_cooldown.active:
            self.dash_duration.activate()
            self.dash_cooldown.activate()
            return True
    
    def attack(self):
        if not self.attack_cooldown.active:
            self.attack_cooldown.activate()
            print("whoosh") # create a hitbox sprite class

    def update(self, dt):
        self.x_move_timer.update()
        self.dash_duration.update()
        self.dash_cooldown.update()
        self.attack_cooldown.update()
        self.input()
        self.move(dt)
        super().update(dt)

        # animation state
        if self.on_floor and (self.on_wall_left or self.on_wall_right):
            self.set_action("idle")
        elif self.dash_duration.active:
            self.set_action("dash")
        elif self.on_wall_left or self.on_wall_right:
            self.set_action("wall_slide")
        elif not self.on_floor:
            self.set_action("jump")
        elif self.direction.x != 0:
            self.set_action("run") 
        else:
            self.set_action("idle")

