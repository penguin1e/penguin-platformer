"""
Player class for the penguin character.
Handles player movement, jumping, gliding, and collision detection.
"""

import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    """
    Player sprite class representing the penguin character.
    Manages player movement, physics, and state.
    """
    def __init__(self, pos):
        super().__init__()
        # Create player image (temporary rectangle)
        self.image = pygame.Surface((40, 50))  # Width 40, height 50 to match platform height
        self.image = pygame.image.load("images/penguinplayer.png")  # Load penguin image
        self.image = pygame.transform.scale(self.image, (40, 50))  # Scale to match platform height
        self.rect = self.image.get_rect(topleft=pos)
        self.i = self.image
        
        # Player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = PLAYER_SPEED
        self.gravity = PLAYER_GRAVITY
        self.jump_speed = PLAYER_JUMP_FORCE
        
        # Player states
        self.facing_right = True
        self.on_ground = False
        self.gliding = False
        self.can_glide = True  # New flag to control glide availability
        self.jump_timer = 0    # Timer for jump-glide cooldown
        
        # Jump control variables
        self.jump_held = False
        self.jump_hold_time = 0
        self.max_jump_hold = 0.3  # Maximum time jump can be held for max height
        self.min_jump_force = PLAYER_JUMP_FORCE * 0.5  # Reduced to half
        self.max_jump_force = PLAYER_JUMP_FORCE * 0.75  # Reduced to half of 1.5x
        
        # Glide settings
        self.glide_speed = 2  # Horizontal speed while gliding
        self.glide_gravity = 0.05  # Reduced from 0.5 for longer air time
        self.glide_boost = 0.1  # Reduced from 0.3 for more controlled upward movement
        self.max_glide_boost = 0.4  # Maximum upward velocity while gliding
        
    def get_input(self):
        """
        Handles keyboard input for player movement.
        Controls horizontal movement, jumping, and gliding.
        """
        keys = pygame.key.get_pressed()
        
        # Horizontal movement
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
            
        else:
            self.direction.x = 0
            
        # Handle jump input
        if keys[pygame.K_z]:
            if not self.jump_held and self.on_ground:
                self.jump()
                self.jump_held = True
                self.jump_hold_time = 0
            elif self.jump_held and not self.on_ground:
                # Continue applying jump force while key is held
                self.jump_hold_time += 1/60  # Assuming 60 FPS
                if self.jump_hold_time < self.max_jump_hold:
                    # Gradually reduce jump force over time
                    jump_force = self.max_jump_force - (self.jump_hold_time / self.max_jump_hold) * (self.max_jump_force - self.min_jump_force)
                    self.direction.y = jump_force
        else:
            self.jump_held = False
            self.jump_hold_time = 0
            
        # Glide
        if keys[pygame.K_g] and not self.on_ground and self.can_glide:
            self.gliding = True
        else:
            self.gliding = False
            
    def apply_gravity(self):
        """
        Applies gravity to the player.
        Handles different gravity values for normal falling and gliding.
        """
        if self.gliding:
            # Apply reduced gravity with controlled upward boost
            if self.direction.y < 0:  # Only apply boost when moving upward
                # Limit the upward velocity while gliding
                if self.direction.y > -self.max_glide_boost:
                    self.direction.y += self.glide_boost
            else:
                self.direction.y += self.glide_gravity
                
            # Maintain horizontal movement
            if self.facing_right:
                self.direction.x = self.glide_speed
            else:
                self.direction.x = -self.glide_speed
        else:
            # Normal gravity when not gliding
            self.direction.y += self.gravity
        self.rect.y += self.direction.y
        
    def jump(self):
        """
        Makes the player jump by applying upward force.
        Resets glide state when jumping.
        """
        self.direction.y = self.max_jump_force  # Start with max jump force
        self.gliding = False
        self.can_glide = False
        self.jump_timer = 0.2
        
    def update(self):
        """
        Updates player state each frame.
        Handles input and sprite flipping based on direction.
        """
        # Update jump timer
        if not self.can_glide:
            self.jump_timer -= 1/60  # Assuming 60 FPS
            if self.jump_timer <= 0:
                # Only re-enable glide when starting to fall
                if self.direction.y >= 0:
                    self.can_glide = True
                    
        self.get_input()
        self.image = pygame.transform.flip(self.i, not self.facing_right, 0)

        # Don't apply gravity here, let the level handle it 