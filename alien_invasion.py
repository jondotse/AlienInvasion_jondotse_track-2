"""
Program Name: alien_invasion.py
Author: Jonathan Dotse
Purpose: Main entry point and what controlls the Alien Invasion game. Initializes pygame, the screen,
settings, sound, and all game objects. It runs the core game loop, events, updates, collsions, and rendering. 
Starter Code: Based on the Alien Invasion tutorial starter code, originally cloned from
    https://github.com/jondotse/alien_Invasion_starter.git
Date: August 2, 2026
"""
import sys
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from arsenal import Arsenal
#from alien import Alien
from alien_fleet import AlienFleet
from time import sleep
from button import Button
from hud import HUD

class AlienInvasion:
    """Main game controller class. Owns the screen, settings, sound, ship
    alien fleet, HUD, and play the button, and runs the primary game loop: event
    handling, state updates, collision checks, and rendering."""

    def __init__(self):
        """Initialize pygame, load settings and assets, and construct all core game objects
        (ship, alien fleet, HUD, sounds, play button)."""
        pygame.init()
        self.settings = Settings()
        self.settings.initialize_dynamic_settings()

        self.screen = pygame.display.set_mode((self.settings.screen_w,self.settings.screen_h))
        pygame.display.set_caption(self.settings.name)

        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg, (self.settings.screen_w, self.settings.screen_h))

        self._game_stats = GameStats(self)
        self.HUD = HUD(self)
        self.running = True
        self.clock = pygame.time.Clock()

        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(self.settings.laser_sound)
        self.laser_sound.set_volume(0.7)

        self.impact_sound = pygame.mixer.Sound(self.settings.impact_sound)
        self.impact_sound.set_volume(0.7)

        pygame.mixer.music.load(self.settings.music_file)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        self.ship = Ship(self, Arsenal(self))
        self.alien_fleet = AlienFleet(self)
        self.alien_fleet.create_fleet()

        self.play_button = Button(self, '')
        self.game_active = False

    def run_game(self):
        """Run the main game loop: process events, update game state when active,
        check collisions, and render each frame at the configured FPS."""
        # Game loop
        while self.running:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self.alien_fleet.update_fleet()
                self._check_collisions()
            self._update_screen()
            self.clock.tick(self.settings.FPS) 

    def _check_collisions(self):
        """Check all collision conditions each frame: ship vs alien, alien fleet vs
        bottom of the screen, and bullets vs aliens. Also update game stats, HUD, and trigger level
        progression when the fleet is destroyed."""
       # check collisions for ship
        if self.ship.check_collisions(self.alien_fleet.fleet):
            self._check_game_status()
            # substract one life if possible

       # check collisions for aliens and bottom of screen
        if self.alien_fleet.check_fleet_bottom():
            self._check_game_status()

       # check collisions of projects and aliens
        collisions = self.alien_fleet.check_collisions(self.ship.arsenal.arsenal)
        if collisions:
            self.impact_sound.play()
            self.impact_sound.fadeout(500)
            self._game_stats.update(collisions)
            self.HUD.update_scores()

        if self.alien_fleet.check_destroyed_status():
            self._reset_level()
            self.settings.increase_difficulty()
            # update game stats level
            self._game_stats.update_level()
            # update HUD view
            self.HUD.update_level()
       
    def _check_game_status(self):
        """Handle a life-losing collision: decrement ships remaing and reset the level if lives
        remain, or end the active game."""

        if self._game_stats.ships_left > 0:
            self._game_stats.ships_left -= 1
            self._reset_level()
            sleep(0.5)
        else:
            self.game_active = False

        #print(self._game_stats.ships_left)

    def _reset_level(self):
        """Clear all active bullets and aliens, then rebuild a fresh alien fleet."""
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_fleet()

    def restart_game(self):
        """Reset dynamic settings, stats, HUD, and the level to start a brand-new game
        session, then set the game to active."""
        self.settings.initialize_dynamic_settings()
        self._game_stats.reset_stats()
        self.HUD.update_scores()
        self._reset_level()
        self.ship._center_ship()
        self.game_active = True
        pygame.mouse.set_visible(False)

    def _update_screen(self):
        """Draw the background, ship, alien fleet, and HUD each frame.
        Show the play button and mouse cursor when game is not active."""
        self.screen.blit(self.bg, (0,0))
        self.ship.draw()
        self.alien_fleet.draw()
        self.HUD.draw()

        if not self.game_active:
            self.play_button.draw()
            pygame.mouse.set_visible(True)

        pygame.display.flip()

    def _check_events(self):
        """Process the pygame event queue each frame: handle window close, keydown/keyup
        input (only when the game is active for keydown), and mouse clicks on the play button."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self._game_stats.save_scores()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and self.game_active == True:
                self._checK_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._checK_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_button_clicked()

    def _check_button_clicked(self):
        """Check whether the play button was clicked and restart the game if so."""
        mouse_pos = pygame.mouse.get_pos()
        if self.play_button.check_clicked(mouse_pos):
            self.restart_game()

    def _checK_keyup_events(self, event):
        """Stop ship movement when the right or left arrow key is released."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False


    def _checK_keydown_events(self, event):
        """Handle key presses: move the ship, fire a bullet with sound on spacebar, or
        quit the game on 'Q'."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            if self.ship.fire():
               self.laser_sound.play()
               self.laser_sound.fadeout(250) 

        elif event.key == pygame.K_q:
            self.running = False
            self._game_stats.save_scores()
            pygame.quit()
            sys.exit() 



if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()