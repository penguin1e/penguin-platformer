"""
Level class for managing the game world.
Handles platform creation, collision detection, and camera movement.
"""

import pygame
from settings import *
from player import Player
from camera import Camera

class Level:
    """
    Manages the game level including platforms, player, and camera.
    Handles collision detection and world updates.
    """
    def __init__(self):
        # Get the display surface
        self.display_surface = pygame.display.get_surface()
        
        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        
        # Setup camera
        self.camera = Camera(LEVEL_WIDTH, LEVEL_HEIGHT)
        
        # Load platform images
        self.ice_block = pygame.image.load("images/iceblock.png").convert_alpha()
        self.ice_block = pygame.transform.scale(self.ice_block, (50, 50))
        self.ice_block_width = self.ice_block.get_width()
        self.ice_block_height = self.ice_block.get_height()
        
        self.dirt_block = pygame.image.load("images/iceblock.png").convert_alpha()
        self.dirt_block = pygame.transform.scale(self.dirt_block, (50, 50))
        self.dirt_block_width = self.dirt_block.get_width()
        self.dirt_block_height = self.dirt_block.get_height()
        
        # Setup
        self.setup_level()
        
    def create_platform(self, x, y, width, is_ground=False):
        """
        Creates a platform by tiling blocks.
        Args:
            x: x-coordinate of platform
            y: y-coordinate of platform
            width: width of platform in pixels
            is_ground: whether this is a ground platform (uses dirt blocks)
        """
        block = self.dirt_block if is_ground else self.ice_block
        block_width = self.dirt_block_width if is_ground else self.ice_block_width
        block_height = self.dirt_block_height if is_ground else self.ice_block_height
        
        num_blocks = width // block_width
        if width % block_width != 0:
            num_blocks += 1
            
        platform_surface = pygame.Surface((num_blocks * block_width, block_height), pygame.SRCALPHA)
        
        for i in range(num_blocks):
            platform_surface.blit(block, (i * block_width, 0))
            
        platform = pygame.sprite.Sprite()
        platform.image = platform_surface
        platform.rect = platform.image.get_rect(topleft=(x, y))
        return platform
        
    def setup_level(self):
        """
        Initializes the level by creating the player and platforms.
        Sets up the ground and floating platforms.
        """
        # Create player
        self.player = Player((100, 300))
        self.all_sprites.add(self.player)
        
        # Create ground platform using tiled dirt blocks
        ground = self.create_platform(0, LEVEL_HEIGHT - 50, LEVEL_WIDTH, is_ground=True)
        self.platforms.add(ground)
        self.all_sprites.add(ground)
        
        # Create some additional platforms
        platform_positions = [
            (500, 500),
            (1000, 400),
            (1500, 300),
            (2000, 500),
            (2500, 400),
            (3000, 300),
            (3500, 500),
            (4000, 400),
            (4500, 300),
            (5000, 500),
        ]
        
        for x, y in platform_positions:
            platform = self.create_platform(x, y, 200)  # 200 is the width of floating platforms
            self.platforms.add(platform)
            self.all_sprites.add(platform)
        
    def handle_movement(self):
        """
        Handles player movement and collision detection.
        Manages horizontal and vertical movement, including platform collisions.
        """
        player = self.player
        
        # Handle horizontal movement
        player.rect.x += player.direction.x * player.speed

        # Keep player within level boundaries
        if player.rect.left < 0:
            player.rect.left = 0
        if player.rect.right > LEVEL_WIDTH:
            player.rect.right = LEVEL_WIDTH
            
        # Handle vertical movement
        player.apply_gravity()
        
        # Keep player within level boundaries vertically
        if player.rect.top < 0:
            player.rect.top = 0
            player.direction.y = 0
        if player.rect.bottom > LEVEL_HEIGHT:
            player.rect.bottom = LEVEL_HEIGHT
            player.direction.y = 0
            player.on_ground = True
        
        # Check vertical collisions
        player.on_ground = False
        for sprite in self.platforms.sprites():
            if sprite.rect.colliderect(player.rect):
                # Check if collision is from above (player is falling)
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                # Check if collision is from below (player is jumping)
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    
                # Additional check for standing on platform
                if player.rect.bottom == sprite.rect.top and \
                   player.rect.right > sprite.rect.left and \
                   player.rect.left < sprite.rect.right:
                    player.on_ground = True
        
    def update(self):
        """
        Updates the level state each frame.
        Handles player updates and camera movement.
        """
        # Update player input
        self.player.update()
        
        # Handle all movement and collisions
        self.handle_movement()
        
        # Update camera
        self.camera.update(self.player)
        
    def draw(self, surface):
        """
        Draws the level to the screen.
        Renders all sprites with camera offset.
        """
        # Draw background
        surface.fill(SKY_COLOR)
        
        # Draw all sprites with camera offset
        for sprite in self.all_sprites:
            surface.blit(sprite.image, self.camera.apply(sprite)) 