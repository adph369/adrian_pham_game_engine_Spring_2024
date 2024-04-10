# This file was created by Adrian Pham

# loop through a list

FPS = 30

import pygame as pg
clock = pg.time.Clock()

frames = ["frame1", "frame2", "frame3", "frame4"]

frames_length = len(frames)
current_frame = 0

while True:
    clock.tick(FPS)
    now = pg.time.get_ticks()
    then = 0
    if now - then > 1000:
        # print(now)
        then = now 
        current_frame += 1
        print(frames[current_frame%frames_length])
# write a loop thatprints in terminal each frame
        