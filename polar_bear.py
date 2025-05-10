import pygame

# Create polar bear class
class PolarBear(pygame.sprite.Sprite):
    def __init__(self, speed):
        self.speed = speed
        self.image = pygame.image.load("images/polarbear.png")
        self.image = pygame.transform.scale(self.image, (40, 50))
        self.i = self.image
        self.right = True