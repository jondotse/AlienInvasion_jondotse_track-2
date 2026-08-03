"""
Program Name: arsenal.py
Author: Jonathan Dotse
Purpose: Defines the Arsenal class, which manages the active bullets fired by the player, updating
their positions, updating the arsenal, and removing the bullets that have moved off-screen
Starter Code: Based on the Alien Invasion tutorial starter code, originally cloned from
    https://github.com/jondotse/alien_Invasion_starter.git
Date: August 2, 2026
"""

import pygame
from typing import TYPE_CHECKING
from bullet import Bullet

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    

class Arsenal:
    """Manages the group of active bullets fired, handling limit of fired bullets
    """
    def __init__(self, game: 'AlienInvasion'):
        """Initialize a sprite group to hold active bullets."""
        self.game = game
        self.settings = game.settings
        self.arsenal = pygame.sprite.Group()

    def update_arsenal(self):
        """Update all positions of active bullets and remove any that have moved
        off the top of the screen"""
        self.arsenal.update()
        self._remove_bullets_offscreen()

    def _remove_bullets_offscreen(self):
        """Remove any bullet from arsenal whose bottom has went off the screen"""
        for bullet in self.arsenal.copy():
            if bullet.rect.bottom <= 0:
                self.arsenal.remove(bullet)


    def draw(self):
        """Draw every active fired bullet to the screen"""
        for bullet in self.arsenal:
            bullet.draw_bullet()

    def fire_bullet(self):
        """Fire a new bullet if the arsenal hasn't reached its maximum count"""
        if len(self.arsenal) < self.settings.bullet_amount:
            new_bullet = Bullet(self.game)
            self.arsenal.add(new_bullet)
            return True
        return False
        
