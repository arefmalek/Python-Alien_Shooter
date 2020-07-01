import sys

import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard


import game_functions as gf
from button import Button

from ship import Ship
from alien import Alien
from bullet import Bullet

def run_game():
    #initialize game and create a sceen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Make the Play button.
    play_button = Button(ai_settings, screen, "Play")

    # Create an instance to store game statistics and create a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    
    #make a ship, the bullets we use, and aliens to shoot
    ship = Ship(ai_settings, screen)
    #star = Star(ai_settings, screen)
    #group for bullets to be stored in, then grp for aliens
    bullets = Group()
    aliens = Group() 
   #stars and rain for the background
    stars = Group()
    rain = Group()
      
    #making the background and a line or fleet of aliens
    gf.create_background_image(ai_settings, screen, stars)
    gf.create_rain_grid(ai_settings, screen, rain)
    gf.create_fleet(ai_settings, screen, ship, aliens)
            
    # Start the main loop for the game.
    while True:
        #Watch for keyboard and mouse events.
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
                      bullets)

        if stats.game_active:
            #checking for movement
            ship.update()  
            # Redraw the screen during each pass through the loop.      
            # Make the most recently drawn screen visible.
            gf.rain_falling(ai_settings, rain)
            gf.update_bullets(
                ai_settings, screen, ship, aliens, bullets, stats, sb)
            gf.update_aliens(
                ai_settings, stats, screen, ship, aliens, bullets, sb)

        gf.update_screen(ai_settings, screen, ship, aliens, bullets, stars,
                         rain, stats, play_button, sb)

run_game()
