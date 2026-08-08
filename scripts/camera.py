import pygame


class Camera: # Camera no arguments
    def __init__(self):
        self.offset = pygame.Vector2()
        self.display_surface = pygame.display.get_surface()

        # drag
        self.camera_center = pygame.Vector2()
        self.drag_speed = 5 # lower value = more drag
        
        # look ahead
        self.look_ahead_offset = pygame.Vector2()
        self.look_ahead_amount = 150
        self.look_ahead_drag = 10
    
    # update():
    def update(self, target_position, target_direction, dt): # target would in this case be the player
        target = pygame.Vector2(target_position)
        
        # look ahead. to make it omndirectional, use the whole target_direction vector. not just x
        desired_look_ahead = pygame.Vector2(target_direction.x, 0) * self.look_ahead_amount
        self.look_ahead_offset += (desired_look_ahead - self.look_ahead_offset) * min(self.look_ahead_drag * dt, 1)
        
        camera_target = target + self.look_ahead_offset
        # drag
        self.camera_center += (camera_target - self.camera_center) * min(self.drag_speed * dt, 1)
        
        # offset
        self.offset.x = -(self.camera_center.x - self.display_surface.get_width()/2)
        self.offset.y = -(self.camera_center.y - self.display_surface.get_height()/2)
