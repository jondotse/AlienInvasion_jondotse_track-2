"""
Program Name: alien.py
Author: Jonathan Dotse
Purpose: Defines the Alien class, a pygame sprite representing an alien in the fleet,
handling its image, position and movement.
Starter Code: Based on the Alien Invasion tutorial starter code, originally cloned from
    https://github.com/jondotse/alien_Invasion_starter.git
Date: August 2, 2026
"""

import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_fleet import AlienFleet


class Alien(Sprite):
    """Represents a single alien sprite within the fleet. Handles loading and scaling images.
    Also track position, movement and detect if it reaches the edge of the screen."""

    def __init__(self, fleet: 'AlienFleet', x:float, y:float):
        """Initialize the alien's image, size, and starting position"""
        super().__init__()
        self.fleet = fleet
        self.screen = fleet.game.screen
        self.boundaries = fleet.game.screen.get_rect()
        self.settings = fleet.game.settings

        self.image = pygame.image.load(self.settings.alien_file)
        self.image = pygame.transform.scale(self.image, 
            (self.settings.alien_w,self.settings.alien_h)
            )
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def update(self):
        """Move the alien horizotally based on the fleet's current speed and direction"""
        temp_speed = self.settings.fleet_speed

        #if self.check_edges():
            # self.settings.fleet_direction *= -1
            #self.y += self.settings.fleet_drop_speed

        self.x += temp_speed * self.fleet.fleet_direction
        self.rect.x = self.x
        self.rect.y = self.y

    def check_edges(self):
        """Check if the alien has reached the left or right edge of the screen"""
        return (self.rect.right >= self.boundaries.right or self.rect.left <= self.boundaries.left)


    def draw_alien(self):
        """Draw the alien's image to the screen at its current position"""
        self.screen.blit(self.image, self.rect)
