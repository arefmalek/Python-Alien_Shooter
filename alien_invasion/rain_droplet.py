import pygame

from pygame.sprite import Sprite

class Raindrop(Sprite):#if you want to make this a sprite add "Sprite" in parenth
    """A class to represent a single star in the fleet."""
    def __init__(self, ai_settings, screen):
        """Initialize the raindrop and set its starting position."""
        #we call super() to inherit properly from Sprite
        super(Raindrop, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('images/raindrop.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # Store the alien's exact position.
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)
