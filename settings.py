"""
Program Name: settings.py
Author: Jonathan Dotse
Purpose: Defines the Settings class, which centralizes configuration values for the Alien 
invasion game, including the screen size, assets file, sizing of the fleet, colors and difficulty.
Starter Code: Based on the Alien Invasion tutorial starter code, originally cloned from
    https://github.com/jondotse/alien_Invasion_starter.git
Date: August 2, 2026
"""

from pathlib import Path
BASE_DIR = Path(__file__).parent

class Settings:
    """Has all configuration values through the game, like fixed settings
    (screen size, asset paths) and settings that change across levels(speed, difficulty)."""
    
    def __init__(self):
        """Initialize fixed, unchanging settings: screen dimemsions, 
        asset file paths, sprite dimensions, and colors."""
        self.name: str = 'Alien Invasion - Track 2'
        self.screen_w = 1200
        self.screen_h = 800
        self.FPS = 60
        self.bg_file = BASE_DIR / 'Assets' / 'images' / 'skybox-space.png'
        self.difficulty_scale = 1.1
        self.scores_file = BASE_DIR / 'Assets' / 'file' / 'scores.json'

        self.ship_file = BASE_DIR / 'Assets' / 'images' / 'spaceShips_005.png'
        self.ship_w = 60
        self.ship_h = 80

        self.bullet_file = BASE_DIR / 'Assets' / 'images' / 'spaceMissiles_038.png'
        self.laser_sound = BASE_DIR / 'Assets' / 'sound' / 'laser.mp3' 
        self.impact_sound = BASE_DIR / 'Assets' / 'sound' / 'impactSound.mp3' 

        self.alien_file = BASE_DIR /'Assets' / 'images' / 'spaceAstronauts_010.png'
        self.alien_w = 40
        self.alien_h = 40
        self.fleet_direction = 1

        self.button_w = 200
        self.button_h = 50
        self.button_color = (0,135,50)

        self.text_color = (255,255,255)
        self.button_font_size = 48
        self.HUD_font_size = 20
        self.font_file = BASE_DIR / 'Assets' / 'Fonts' / 'Silkscreen' / 'Silkscreen-Bold.ttf'

    def initialize_dynamic_settings(self):
        """Initialize settinsg that change during the game(speeds, bullet size, and behavior of the fleet)."""
        self.ship_speed = 5
        self.starting_ship_count = 3

        self.bullet_w = 18
        self.bullet_h = 45
        self.bullet_speed = 7
        self.bullet_amount = 5

        self.fleet_speed = 2
        self.fleet_drop_speed = 30
        self.alien_points = 50

    def increase_difficulty(self):
        """Scale up the  ship, bullet, and fleet speed by difficulty_scale, making the game
        harder bit by bit as the player advances."""
        self.ship_speed *= self.difficulty_scale
        self.bullet_speed *= self.difficulty_scale
        self.fleet_speed *= self.difficulty_scale