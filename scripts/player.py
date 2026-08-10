import pygame

from scripts.support import move_toward
from scripts.sprites import Sprite, AnimatedSprite
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


class Hitbox(Sprite):
    def __init__(self, pos, size, groups, player): # add enemies later
        self.surf = pygame.Surface(size)
        self.surf.fill((255,255,255))
        self.surf.set_alpha(100)
        super().__init__(pos, self.surf, groups)
        self.player = player
        self.duration = Timer(300, func=self.kill, autostart=True) 
    
    # kill enemy

    def update(self, dt):
        self.duration.update()


class Player(AnimatedSprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(pos, PLAYER_ANIMATIONS, groups)
        
        # movement & collision
        self.collision_sprites = collision_sprites 
        self.gravity = 48 
        self.direction = pygame.Vector2()
        self.on_surface = {"floor": False, "left": False, "right": False}

        self.max_speed = 430
        self.velocity_x = 0
        self.floor_accel = 3000
        self.air_accel = 1500 
        
        # timers
        self.timers = {
            "x_move": Timer(300),
            "dash_duration": Timer(150),
            "dash_cooldown": Timer(500),
            "attack_cooldown": Timer(750),
        }

        self.old_rect = self.rect.copy()
        
    def input(self):
        keys = pygame.key.get_pressed()
        just_pressed = pygame.key.get_just_pressed()

        if just_pressed[pygame.K_UP]:
            self.jump()

        if just_pressed[pygame.K_x] and not self.timers["dash_duration"].active:
            self.dash()

        if keys[pygame.K_z] and not self.timers["attack_cooldown"].active:
            self.attack()

        if not self.timers["x_move"].active and not self.timers["dash_duration"].active:
            self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])

    def aim_direction(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            return pygame.Vector2(0,-1)
        if keys[pygame.K_DOWN]:
            return pygame.Vector2(0,1)
        if keys[pygame.K_RIGHT]:
            return pygame.Vector2(1,0)
        if keys[pygame.K_LEFT]:
            return pygame.Vector2(-1,0)
        return pygame.Vector2(-1,0) if self.flip else pygame.Vector2(1,0)
            
    def move(self, dt):
        if self.timers["dash_duration"].active:
            #self.direction.x = -1 if self.flip else 1
            self.direction.y = 0
            if self.direction.x == 0: 
                self.direction.x = -1 if self.flip else 1
            self.velocity_x = self.direction.x * (self.max_speed * 1.5)
            self.rect.x += self.velocity_x * dt
        else:
            accel = self.floor_accel if self.on_surface["floor"] else self.air_accel
            target_velocity = self.direction.x * self.max_speed
            self.velocity_x = move_toward(self.velocity_x, target_velocity, accel * dt)

            if self.velocity_x > 0: self.flip = False
            if self.velocity_x < 0: self.flip = True 
            
            self.rect.x += self.velocity_x * dt
        
        self.collision("horizontal")
        
        # vertical velocity
        self.direction.y += self.gravity * dt
        self.direction.y = min(self.direction.y, 500) # terminal velocity
        self.rect.y += self.direction.y
        self.collision("vertical")

    def check_contact(self):
        floor_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, 2))
        right_rect = pygame.Rect(self.rect.topright + pygame.Vector2(0, self.rect.height / 4), (2, self.rect.height / 2))
        left_rect = pygame.Rect(self.rect.topleft + pygame.Vector2(-2, self.rect.height / 4), (2, self.rect.height / 2))

        collide_rects = [sprite.rect for sprite in self.collision_sprites]
        self.on_surface["floor"] = floor_rect.collidelist(collide_rects) >= 0
        self.on_surface["right"] = right_rect.collidelist(collide_rects) >= 0
        self.on_surface["left"] = left_rect.collidelist(collide_rects) >= 0

    def collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if axis == "horizontal":
                    if not self.on_surface["floor"] and (self.on_surface["left"] or self.on_surface["right"]) and self.direction.y > 0:
                        self.direction.y *= 0.65
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.rect.right:
                        self.rect.left = sprite.rect.right
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.rect.left:
                        self.rect.right = sprite.rect.left 
                elif axis == "vertical":
                    if self.direction.y > 0 and self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.direction.y = 0
                    if self.direction.y < 0 and self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.direction.y = 0

    def jump(self):
        if self.on_surface["floor"]:
            self.direction.y = -12
            return True
        if self.on_surface["left"]:
            self.direction.y = -12
            self.direction.x = 1
            self.velocity_x = self.max_speed
            self.timers["x_move"].activate()
            return True
        if self.on_surface["right"]:
            self.direction.y = -12
            self.direction.x = -1
            self.velocity_x = -self.max_speed
            self.timers["x_move"].activate()
            return True
    
    def dash(self):
        if not self.timers["dash_cooldown"].active:
            self.timers["dash_duration"].activate()
            self.timers["dash_cooldown"].activate()
            return True
    
    def attack(self):
        if not self.timers["attack_cooldown"].active:
            self.timers["attack_cooldown"].activate()
            aim = self.aim_direction()

            if aim.y > 0 and self.on_surface["floor"]:
                print("cant attack lmao")
                return

            if aim.x != 0:
                size = (70,50)
                self.attack_action = "attack"
            elif aim.y < 0:
                size = (50,70)
                self.attack_action = "attack_up"
            elif aim.y > 0:
                size = (50,70)
                self.attack_action = "attack_down"

            offset = pygame.Vector2(aim.x * (self.rect.width / 2 + size[0] / 2), aim.y * (self.rect.height / 2 + size[1] / 2))
            hitbox_center = pygame.Vector2(self.rect.center) + offset
            hitbox_pos = (hitbox_center.x - size[0] / 2, hitbox_center.y - size[1] / 2)
            Hitbox(hitbox_pos, size, self.groups(), self)
            return True
    
    def update_timers(self):
        for timer in self.timers.values():
            timer.update()
    
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.update_timers()
        self.input()
        self.move(dt)
        self.check_contact()
        super().update(dt)

        # animation state
        # first is going to be attack   
        if self.on_surface["floor"] and (self.on_surface["left"] or self.on_surface["right"]):
            self.set_action("idle")
        elif self.timers["dash_duration"].active:
            self.set_action("dash")
        elif self.on_surface["left"] or self.on_surface["right"]:
            self.set_action("wall_slide")
        elif not self.on_surface["floor"]:
            self.set_action("jump")
        elif self.direction.x != 0:
            self.set_action("run")
        else:
            self.set_action("idle")
