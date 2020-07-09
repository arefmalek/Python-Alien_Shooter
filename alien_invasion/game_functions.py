import sys
#this module used to pause game
from time import sleep

import pygame
from random import randint

from bullet import Bullet
from alien import Alien
from background_star import Star
from rain_droplet import Raindrop

def create_background_image(ai_settings, screen, stars):
    """Create a full line of background stars."""
    # Create a star and find the number of stars in a row.
    # Spacing between each star is equal to one star width.
    star = Star(ai_settings, screen)
    #star measurements
    star_width = star.rect.width
    star_height = star.rect.height

    #for the x direction (number of stars)
    available_space__stars_x = ai_settings.screen_width - 1.5 * star_width
    number_stars_x = int(available_space__stars_x / (1.5 * star_width))
    #for the y direction (number of rows)
    available_star_space_y=  (ai_settings.screen_height - (star_height))
    number_star_rows = int(available_star_space_y / (1.5 * star_height))
    
    # Create the grid of stars.
    for star_row_number in range(number_star_rows):
        for star_number in range(number_stars_x):
            # Create an alien and place it in the row.
            random_number = randint(-50,50)
            star = Star(ai_settings, screen)
            star.x = star_width + 1.5 * star_width * star_number
            star.rect.x = star.x + random_number
            star.y = (star.rect.height +
                            (1.5 * star.rect.height * star_row_number))

            star.rect.y = star.y +random_number
            stars.add(star)

def create_rain_grid(ai_settings, screen, rain):
    """Create a full grid of background rain."""
    # Create a Raindrop and find the number of stars in a row.
    # Spacing between each star is equal to one star width.
    raindrop = Raindrop(ai_settings, screen)
    #star measurements
    raindrop_width = raindrop.rect.width
    raindrop_height = raindrop.rect.height

    #for the x direction (number of stars)
    available_space_rain_x = ai_settings.screen_width
    number_raindrop_x = int(available_space_rain_x / (raindrop_width))
    #for the y direction (number of rows)
    available_space_rain_y = (ai_settings.screen_height - (raindrop_height))
    number_rain_rows = int(available_space_rain_y / (raindrop_height))
    
    # Create the grid of stars.
    for rain_row_number in range(number_rain_rows):
        for rain_number in range(number_raindrop_x):
            # Create an alien and place it in the row.
            random_number = randint(-50,50)
            raindrop = Raindrop(ai_settings, screen)
            raindrop.x = raindrop_width * rain_number
            raindrop.rect.x = raindrop.x + random_number
            raindrop.y = (raindrop.rect.height * rain_row_number)

            raindrop.rect.y = raindrop.y + random_number
            rain.add(raindrop)
    
def update_rainfall(ai_settings, screen, rain):
    """Drops all of the rain then checks the status of rainfall"""
    for raindrop in rain.sprites():
        raindrop.rect.y += ai_settings.rainfall_speed
        
    #Update rain positions
    rain.update()

    #get rid of bullets that are out of the screen
    for raindrop in rain.copy():
        if raindrop.rect.top >= ai_settings.screen_height:
            rain.remove(raindrop)

    if len(rain) == 0:
        #if entire fleet is destroyed, start a new level
            create_rain_grid(ai_settings, screen, rain)

def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
 
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):

    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    alien = Alien(ai_settings, screen)
    
    #calls two diff functions to return values for later use
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    # Create the fleet row of aliens.
    for row_number in range(number_rows):
        #this gives you each line of aliens
            for alien_number in range(number_aliens_x):
                create_alien(
                    ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.border_patrol():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:

        # Decrement ships_left.
        stats.ships_left -= 1

        #update the scoreboard
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)

        #DEBUGG!!! DOESNT MOVE TO CENTER-BOTTOM OF SCREEN
        ship.center_ship()

        # Pause.
        sleep(0.5)


        print(stats.ships_left)
        print(stats.game_active)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
            break

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb):

    """
    Check if the fleet is at an edge,
    and then update the postions of all aliens in the fleet.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update(ai_settings)
    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
        print("Ship hit!!!")

    # Look for aliens hitting the bottom of the screen.

    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb)

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """responds to keypresses"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    
def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet."""
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
    

def check_keyup_events(event, ship):
    """responds to keylifts"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False
    elif event.key == pygame.K_q:
        sys.exit()

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
                      bullets):
    """Respond to keyboard activity and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            #start moving ship to the right or left
            check_keydown_events(event, ai_settings, screen, ship, bullets)
            #print(event.key)
            
        elif event.type == pygame.KEYUP:
            #stop moving ship
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                              aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y):

    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()


        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb):
    """Updates position of bullets and gets rid of old bullets."""
    #Update bullet positions
    bullets.update()

    #get rid of bullets that are out of the screen
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
        
    # Check for any bullets that have hit aliens.
    # If so, get rid of the bullet and the alien.
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets,
                                  stats, sb)

    #print(len(bullets))

def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets,
                                  stats, sb):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        #if entire fleet is destroyed, start a new level
        bullets.empty()
        ai_settings.increase_speed()

        #increase level
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)
        
def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def update_screen(ai_settings, screen, ship, aliens, bullets, stars, rain,
                  stats, play_button, sb):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)
    stars.draw(screen)
    rain.draw(screen)
    #redraw bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
        
    #making the alien fleet/ship appear onscreen
    ship.blitme()

    #draw() draws each element in group at position defined by rect attribute
    aliens.draw(screen)

    # Draw the score information.
    sb.show_score()
    
    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()


    # Make the most recently drawn screen visible.
    pygame.display.flip()
