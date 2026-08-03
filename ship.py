"""
Program Name: ship.py
Author: Jonathan Dotse
Purpose: Defines the Ship class, which controls the player's spaceship,
    including movement, rendering, firing, and collision handling for
    the Alien Invasion game (Track 2 - Custom Assets).
Starter Code: Based on the Alien Invasion tutorial starter code, originally cloned from
    https://github.com/jondotse/alien_Invasion_starter.git
Date: August 2, 2026
"""

import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal

class Ship:
    """This represents how the player controlled its ship, handling its position, 
    movement, firing bullets and collision detection against the alien fleet
    """

    def __init__(self, game: 'AlienInvasion', arsenal: 'Arsenal'):
        """Initialize the ship's image, position, and movement.
        """
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()

        self.image = pygame.image.load(self.settings.ship_file)
        self.image = pygame.transform.scale(self.image, 
            (self.settings.ship_w,self.settings.ship_h)
            )
        
        self.rect = self.image.get_rect()
        self._center_ship()
        self.moving_right = False
        self.moving_left = False
        self.arsenal = arsenal

    def _center_ship(self):
        """Defines the initial position of the ship which is
        at the center, bottom edge of the screen"""
        self.rect.midbottom = self.boundaries.midbottom
        self.x = float(self.rect.x)

    def update(self):
        """Update the ship's position and refresh its active bullets"""
        # updating the position of the ship
        self._update_ship_movement()
        self.arsenal.update_arsenal()

    def _update_ship_movement(self):
        """Move the ship left of right based the keyboard input while staying within the 
        screen boundaries."""
        temp_speed = self.settings.ship_speed
        if self.moving_right and self.rect.right < self.boundaries.right:
            self.x += temp_speed
        if self.moving_left and self.rect.left > self.boundaries.left:
            self.x -= temp_speed

        self.rect.x = self.x

    def draw(self):
        """Draw the ship's active bullets and the ship image itself to the screen"""
        self.arsenal.draw()
        self.screen.blit(self.image, self.rect)

    def fire(self):
        """Attempt tp fire a bullet from the ship's arsenal."""
        return self.arsenal.fire_bullet()
    
    def check_collisions(self, other_group):
        """Check if the ship has collided with any sprite"""
        if pygame.sprite.spritecollideany(self, other_group):
            self._center_ship()
            return True
        return False
