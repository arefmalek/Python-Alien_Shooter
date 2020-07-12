import pygame
from pygame.sprite import Sprite


from settings import Settings

class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        """Initialize the ship and set its starting position."""
        super(Ship, self).__init__()

        self.screen = screen
        self.ai_settings = ai_settings

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height

        # Start each new ship at the bottom center of the screen.
        self.rect.x = self.screen_rect.centerx
        self.rect.y = self.screen_rect.centery
        self.rect.midbottom = self.screen_rect.midbottom   

        #storing a decimal value for the ship's center
        self.xdir = float(self.rect.x)
        self.ydir = float(self.rect.y)

        #Movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update the ship's position based on movement flag"""
        #update the ship's center value, not the rect 
        if self.moving_right and self.xdir < (self.ai_settings.screen_width
                                              -self.width):
            self.xdir += self.ai_settings.ship_speed_factor
        if self.moving_left and self.xdir > 0:
            self.xdir -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.ydir > 0:
            self.ydir -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.ydir < (self.ai_settings.screen_height-
                                             self.height):
            self.ydir += self.ai_settings.ship_speed_factor

        #update rect object from the self.center
        self.rect.x = self.xdir
        self.rect.y = self.ydir

    def center_ship(self):
        """Center the ship on the screen."""
        self.xdir = self.screen_rect.centerx
        self.ydir = self.screen_rect.bottom - self.height   

        
    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
