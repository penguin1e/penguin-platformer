import pygame
import sys
from settings import *
from player import Player
from level import Level

class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Penguin Platformer')
        self.clock = pygame.time.Clock()
        
        # Create game objects
        self.level = Level()
        
    def run(self):
        while True:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # Update game state
            self.level.update()
            
            # Draw everything
            self.screen.fill('black')
            self.level.draw(self.screen)
            
            # Update display
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
