# from pathlib import Path
"""
Program Name: game_stats.py
Author: Jonathan Dotse
Purpose: Defines the GameStats class, which tracks the player's current score
ships remaining, and level during gameplay.
Starter Code: Based on the Alien Invasion tutorial starter code, originally cloned from
    https://github.com/jondotse/alien_Invasion_starter.git
Date: August 2, 2026
"""
import json

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class GameStats():
    """Tracks for every session game statistics (score, ships remaining,
    level) and manages loading/saving the persistent high score to a JSON file on 
    disk."""

    def __init__(self, game: 'AlienInvasion'):
        """Initialize game stats by loading the saved high score from disk and
        resetting every session stats."""
        self.game = game
        self.settings = game.settings
        self.max_score = 0
        self.init_saved_scores()
        self.reset_stats()

    def init_saved_scores(self):
        """Load the saved high score from the scores file if it exists and is non-empty; otherwise
        initialize the high socre to 0 and create the file."""
        self.path = self.settings.scores_file 
        if self.path.exists() and self.path.stat().st_size > 0:
            contents = self.path.read_text()
            if not contents:
                print('file empty')
            scores = json.loads(contents)
            self.hi_score = scores.get('hi_score', 0)
        else:
            self.hi_score = 0
            self.save_scores()
            # save the file

    def save_scores(self):
        """Write the current high score to the scores file as JSON."""
        scores = {
            'hi_score': self.hi_score
        }
        contents = json.dumps(scores, indent=4)
        try:
            self.path.write_text(contents)
        except FileNotFoundError as e:
            print(f'File Not Found: {e}')

    def reset_stats(self):
        """Reset the per-sessopn stats (ships remaining, score, level to their starting values. 
        Does not affect the persistent high score.)"""
        self.ships_left = self.settings.starting_ship_count
        self.score = 0
        self.level = 1


    def update(self, collisions):
        """Update the current score, max score, and high score based on the given collision results."""
        # update score
        self._update_score(collisions)
        # update max_score
        self._update_max_score()

        # update hi_score
        self._update_hi_score()

    def _update_max_score(self):
        """Update the session's max score if the current score has surpassed it."""
        if self.score > self.max_score:
            self.max_score = self.score
            # print(f'Max: {self.max_score}')
    def _update_hi_score(self):
        """Update the persistent high score if the current score has surpassed it."""
        if self.score > self.hi_score:
            self.hi_score = self.score
            # print(f'Hi: {self.max_score}')

    def _update_score(self, collisions):
        """Increase the current score based on the number of aliens destroyed in the given collisions."""
        for alien in collisions.values():
            self.score += self.settings.alien_points
        # print(f'Basic: {self.score}')

    def update_level(self):
        """Increment the current level by one."""
        self.level += 1
        #print(self.level)

       
