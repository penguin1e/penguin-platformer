"""
Camera class for managing the game viewport.
Handles screen scrolling and player tracking.
"""

import pygame
from settings import *

class Camera:
    """
    Manages the game camera and viewport.
    Handles smooth scrolling and player tracking.
    """
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.target_x = 0
        self.smooth_speed = 0.1  # Adjust this value to change smoothness (0.0 to 1.0)
        
    def apply(self, entity):
        """
        Applies camera offset to an entity's position.
        Args:
            entity: The sprite to apply camera offset to
        Returns:
            The adjusted position of the entity
        """
        return entity.rect.move(self.camera.topleft)
        
    def update(self, target):
        """
        Updates camera position to follow the target.
        Args:
            target: The sprite to follow (usually the player)
        """
        # Calculate target x position to center the player
        target_x = -target.rect.centerx + SCREEN_WIDTH // 2
        
        # Limit camera to level boundaries
        target_x = min(0, target_x)  # Don't scroll past left edge
        target_x = max(-(self.width - SCREEN_WIDTH), target_x)  # Don't scroll past right edge
        
        # Smoothly interpolate to the target position
        self.camera.x += (target_x - self.camera.x) * self.smooth_speed
        
        # Keep player visible vertically
        if target.rect.top < 0:
            target.rect.top = 0
        if target.rect.bottom > SCREEN_HEIGHT:
            target.rect.bottom = SCREEN_HEIGHT 