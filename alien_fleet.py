"""
Program Name: alien_fleet.py
Author: Jonathan Dotse
Purpose: Defines the AlienFleet class, which creates, positions, moves and manages the entire
group of alien sprites as a single fleet. This includes edge detection, dropping, collision checks, 
and determine when the fleet has been destroyed or reached the bottom of the screen.
Starter Code: Based on the Alien Invasion tutorial starter code, originally cloned from
    https://github.com/jondotse/alien_Invasion_starter.git
Date: August 2, 2026
"""

import pygame
from typing import TYPE_CHECKING
from alien import Alien

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    

class AlienFleet:
    """Manages the full group of alien sprites, including fleet layout, the group movement
    of the fleet, dropping behavior, collision detection and fleet status checks."""

    def __init__(self, game: 'AlienInvasion'):
        """Initialize the fleet's sprite group, direction and drop speed."""
        self.game = game
        self.settings = game.settings
        self.fleet = pygame.sprite.Group()
        self.fleet_direction = self.settings.fleet_direction
        self.fleet_drop_speed = self.settings.fleet_drop_speed

        self.create_fleet()

    def create_fleet(self):
        """Calculate fleet dimensions and offsets based on screen and alien size."""
        alien_w = self.settings.alien_w
        alien_h = self.settings.alien_h
        screen_w = self.game.settings.screen_w
        screen_h = self.settings.screen_h

        fleet_w, fleet_h = self.calculate_fleet_size(alien_w, screen_w, alien_h, screen_h)
        x_offset, y_offset = self.calculate_offsets(alien_w, alien_h, screen_w, fleet_w, fleet_h)

        
        self._create_wedge_fleet(alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset)

    def _create_wedge_fleet(self, alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset):
        """Create aliens in an inverted pyramid formation: the top rows
        has the full fleet width, and each row below it is narrower by one alien on each
        side, converging towoard the center as rows descend."""
        max_rows = min(fleet_h, 6)
        for row in range(max_rows):
            row_indent  =  row * 2
            row_width = fleet_w - (2 * row_indent)
            if row_width <= 0:
                break
            for col in range(row_indent, row_indent + row_width, 2):
                current_x = alien_w * col + x_offset
                row_spacing = alien_h * 1.5
                current_y = row_spacing * row + y_offset
                self._create_alien(current_x, current_y)

    def calculate_offsets(self, alien_w, alien_h, screen_w, fleet_w, fleet_h):
        """Calculate the horizontal and vertical space needed to center the fleet
        within the top half of the screen."""
        half_screen = self.settings.screen_h // 2
        fleet_horizontal_space = fleet_w * alien_w
        fleet_vertical_space = fleet_h * alien_h
        x_offset = int((screen_w -  fleet_horizontal_space) // 2)
        y_offset = int((half_screen-fleet_vertical_space)//2)
        return x_offset,y_offset



    def calculate_fleet_size(self, alien_w, screen_w, alien_h, screen_h):
        """Calculate how many alien columns and rows fit whitin the screen, 
        leaving a margin on each side."""
        fleet_w = (screen_w // alien_w)
        fleet_h = ((screen_h / 2) // alien_h)

        if fleet_w % 2 == 0:
            fleet_w -= 1
        else:
            fleet_w -= 2

        if fleet_h % 2 == 0:
            fleet_h -= 1
        else:
            fleet_h -= 2

        return int(fleet_w), int(fleet_h)
    
    def _create_alien(self, current_x: int, current_y: int):
        """Create a single Alien instance at the given coordinates and add it to the fleet group."""
        new_alien = Alien(self, current_x, current_y)

        self.fleet.add(new_alien)

    def _check_fleet_edges(self):
        """Check whether any alien in the fleet has reached a screen edge."""
        alien: Alien
        for alien in self.fleet:
            if alien.check_edges():
                self._drop_alien_fleet()
                self.fleet_direction *= -1
                break

    def _drop_alien_fleet(self):
        """Move every alien in the fleet down by the configured drop speed. """
        for alien in self.fleet: 
            alien.y += self.fleet_drop_speed

    def update_fleet(self):
        """Check for the edge collisions and update the position of every alien in the fleet."""
        self._check_fleet_edges()
        self.fleet.update()

    def draw(self):
        """Draw every alien currently in the fleet to the screen."""
        alien: 'Alien'
        for alien in self.fleet:
            alien.draw_alien()

    def check_collisions(self, other_group):
        """Check for collisions between the fleet and another sprite group."""
        return pygame.sprite.groupcollide(self.fleet, other_group, True, True)
    
    def check_fleet_bottom(self):
        """Check whether any alien in the fleet has reached the bottom of the screen"""
        alien: Alien
        for alien in self.fleet:
            if alien.rect.bottom >= self.settings.screen_h:
                return True
        return False
    
    def check_destroyed_status(self):
        """Check whether the entire fleet has been destroyed. """
        return not self.fleet