"""
Program Name: button.py
Author: Jonathan Dotse
Purpose: Defines the Button class, a UI button used to start the game. This program handles its 
rectangle, text label, drawing, and click detection
Starter Code: Based on the Alien Invasion tutorial starter code, originally cloned from
    https://github.com/jondotse/alien_Invasion_starter.git
Date: August 2, 2026
"""
import pygame.font

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Button:
    """Represents a clickable rectangular button with a centered text label,
    used for UI interactions such as starting the game."""


    def __init__(self, game: 'AlienInvasion', msg):
        """Initialize the button's size, position, font, and text label. """
        self.game = game
        self.screen = game.screen
        self.boundaries = game.screen.get_rect()
        self.settings = game.settings
        self.font = pygame.font.Font(self.settings.font_file, 
                                     self.settings.button_font_size)
        self.rect = pygame.Rect(0,0,self.settings.button_w, self.settings.button_h)
        self.rect.center = self.boundaries.center
        self._prep_msg(msg)


    def _prep_msg(self, msg):
        """Transfor the text label into an image and center it inside the button's rectangle."""
        self.msg_image = self.font.render(msg, True, self.settings.text_color, None)
        self.msg_image_rect =self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw(self):
        """Draw the button's background rectangle and its text label to the screen."""
        self.screen.fill(self.settings.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def check_clicked(self, mouse_pos):
        """Check whether a given mouse position falls within the button's rectangle."""
        return self.rect.collidepoint(mouse_pos)