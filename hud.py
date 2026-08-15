"""
Program Name: hud.py
Author: Jonathan Dotse
Purpose: Defines the HUD class, which shows the heads-up display, showing the player's 
current score, max score, high score, level and remaining ship available.
Starter Code: Based on the Alien Invasion tutorial starter code, originally cloned from
    https://github.com/jondotse/alien_Invasion_starter.git
Date: August 2, 2026
"""
import pygame.font
#from typing import TYPE_CHECKING

# if TYPE_CHECKING:
#     from alien_invasion import AlienInvasion

class HUD:
    """Manages rendenring of the on-screen heads-up display. Including current score, 
    max score, high score, level indicator, and a row of ship-icon lives remaining"""

    def __init__(self, game):
        """Initialize the HUD's font, spacing, and all text/image elements it will display"""
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = game.screen.get_rect()
        self.game_stats = game._game_stats
        self.font = pygame.font.Font(self.settings.font_file,
                                        self.settings.HUD_font_size)
        self.padding = 10
        self.update_scores()
        self.setup_life_image()
        self.update_level()


    def setup_life_image(self):
         """Load and scale the ship image used to represent remaining lives in the HUD."""
         self.life_image = pygame.image.load(self.settings.ship_file)
         self.life_image = pygame.transform.scale(self.life_image, (
              self.settings.ship_w, self.settings.ship_h
         ))
         self.life_rect = self.life_image.get_rect()

    def update_scores(self):
        """Refresh the rendered images for the current score, high score, and max score"""
        self._update_scores()
        self._update_hi_score()
        self._update_max_score()

    def _update_scores(self):
        """Render the current score text and position it in the top-right area
        of the screen, below the max score."""
        score_str = f'Score: {self.game_stats.score: ,.0f}'
        self.score_image = self.font.render(score_str, True,
                                            self.settings.text_color, None)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.boundaries.right - self.padding
        self.score_rect.top = self.score_rect.bottom + self.padding

    def _update_max_score(self):
        """Render the session/s max score text and position it in the top-right
        corner of the screen."""
        max_score_str = f'Max-Score: {self.game_stats.max_score: ,.0f}'
        self.max_score_image = self.font.render(max_score_str, True,
                                            self.settings.text_color, None)
        self.max_score_rect = self.max_score_image.get_rect()
        self.max_score_rect.right = self.boundaries.right - self.padding
        self.max_score_rect.top = self.padding

    def _update_hi_score(self):
        """Render the persistent high score text and center it along the top of the screen."""
        hi_score_str = f'Hi-Score: {self.game_stats.hi_score: ,.0f}'
        self.hi_score_image = self.font.render(hi_score_str, True,
                                            self.settings.text_color, None)
        self.hi_score_rect = self.hi_score_image.get_rect()
        self.hi_score_rect.midtop = (self.boundaries.centerx, self.padding)

    def update_level(self):
            """Render the current level text and position it below the life icons in the top-left area 
            of the screen."""
            level_str = f'Level: {self.game_stats.level: ,.0f}'
            self.level_image = self.font.render(level_str, True,
                                                self.settings.text_color, None)
            self.level_rect = self.level_image.get_rect()
            self.level_rect.left = self.padding
            self.level_rect.top = self.life_rect.bottom + self.settings.hud_row_gap

    def _draw_lives(self):
        """Draw one ship for each remaining life, arranged in a horizontal row in the top-left corner
        of the screen."""
        current_x = self.padding
        current_y = self.padding
        for _ in range (self.game_stats.ships_left):
             self.screen.blit(self.life_image, (current_x, current_y))
             current_x += self.life_rect.width + self.padding

    def draw(self):
        """Draw all HUD elements (high score, max score, current score, level, and remaining
        lives) to the screen."""
        self.screen.blit(self.hi_score_image,self.hi_score_rect)
        self.screen.blit(self.max_score_image,self.max_score_rect)
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        self._draw_lives()
        
         