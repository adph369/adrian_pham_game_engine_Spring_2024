# This file was created by Adrian Pham with knowledge from Chris Cozort

import pygame as pg 
from math import floor 

# creating a clock countdown
class Timer():
    # sets all to 0 so that when the event is run the timer starts from then
    def __init__(self, game):
        self.game = game
        self.current_time = 0
        self.event_time = 0
        self.cd = 0
    # must use ticking to count time
    def ticking(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
        if self.cd > 0:
            self.countdown()
    # resets event time to zero
    def get_countdown(self):
        return floor(self.cd)
    def countdown(self):
        if self.cd > 0:
            self.cd = self.cd - self.game.dt
    # sets current time
    def get_current_time(self):
        self.current_time = floor((pg.time.get_ticks())/1000)