# This file was created by Adrian Pham with knowledge from Chris Cozort

import pygame as pg 
from math import floor 

# creating a clock countdown
class Timer():
    # sets all to 0 so that when the event is run the timer starts from then
    def __init__(self, game):
        self.game = game
        self.current_time = 0
        self.start_time = 0
        self.event_time = 0
        self.cd = 0
        self.quit_countdown = 0

    # must use ticking to count time
    def ticking(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
        elapsed_time = self.game.dt * (self.current_time - self.start_time)
        if self.cd > 0:
            self.countdown()
        if self.quit_countdown > 0:
            self.quit_timer()


    # resets event time to zero
    def get_countdown(self):
        return floor(self.cd)
    
    def countdown(self):
        if self.cd > 0:
            self.cd -= self.game.dt

    def quit_timer(self):
    # If player dies, start the countdown
        if self.game.player.hp < 0:
            if self.quit_countdown <= 0:
                self.quit_countdown = 5000  # Set quit countdown to 5000 milliseconds (5 seconds)
            else:
                self.quit_countdown -= self.game.dt  # Decrease countdown over time
            if self.quit_countdown <= 0:
                print("Quitting game...")  # Debugging output
                self.game.quit()

    # sets current time
    def get_current_time(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
