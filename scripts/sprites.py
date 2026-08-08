import pygame

from scripts.support import move_toward


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

#    def draw(self, surf, offset=(0, 0)):
#        surf.blit(self.image, (self.rect.x + offset[0], self.rect.y + offset[1]))


class PhysicsSprite(Sprite):
    def __init__(self, pos, speed, animations, groups, collision_sprites):
        self.animations= animations
        self.action = "idle"
        self.frame_index = 0
        self.animation_speed = 10
        self.flip = False
        super().__init__(pos, self.animations[self.action][self.frame_index], groups)
        
        # movement & collision
        self.collision_sprites = collision_sprites 
        self.gravity = 48 
        self.direction = pygame.Vector2()
        self.on_floor = False
        self.max_speed = speed
        self.velocity_x = 0
        self.floor_accel = 3000
        self.air_accel = 1500
        
        # player things i cant build otherwise lol
        self.dash_timer = 0
        self.dash_speed = 900
        
    def move(self, dt):
        self.dash_timer = max(0, self.dash_timer - dt)

        if self.dash_timer > 0:
            self.direction.x = -1 if self.flip else 1
            self.rect.x += self.direction.x * self.dash_speed * dt
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
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.frame_index = 0

    def animate(self, dt):
        frames = self.animations[self.action]
        self.frame_index += self.animation_speed * dt
        self.image = frames[int(self.frame_index) % len(frames)]

#    def draw(self, surf, offset=(0, 0)):
#        display_image = pygame.transform.flip(self.image, self.flip, False)
#        surf.blit(display_image, (self.rect.x + offset[0], self.rect.y + offset[1]))

    def update(self, dt):
        self.move(dt)
        self.animate(dt)
        
