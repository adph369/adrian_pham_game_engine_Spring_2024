# This file was created by: Adrian Pham

# importing necessary libaries

# my first source control edit

# hp bar, game levels, power-ups

import pygame as pg  
from settings import *
from sprites import *
from clock import *
import sys
from random import randint
from os import path 
from math import floor


# creating game class
class Game:
    # initializes all code in a class
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500,100)
        self.load_data()


    # load data, save data, etc.
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        map_folder = path.join(game_folder, 'maps')
        self.player_img = pg.image.load(path.join(img_folder, 'man.png')).convert_alpha()
        self.map_data = []
        with open(path.join(map_folder, 'map1.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)


    def new(self):
        # initialize all variables, setup groups, instantiate classes
        print("Create new game...")
        self.countdown = Timer(self)
        self.all_sprites = pg.sprite.Group()
        self.health = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.door = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        # self.player = Player(self, 10, 10)
        # for x in range(10, 20):
            # Wall(self, x, 5)
        # drawing the game map
        for row, tiles in enumerate(self.map_data):
            # print(self.map_data)
            # print(row)
            # print(tiles)
            # enumerate: assign numbers to terms in a list
            for col, tile in enumerate(tiles):
                # print(col)
                # print(tiles)
                # 1 in map is a wall
                if tile == '1':
                    Wall(self, col, row)
                # P in map is player
                if tile == 'P': 
                    self.player = Player(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'E':
                    Enemy(self, col, row)
                if tile == 'X':
                    Chaser(self, col, row)
                if tile == 'D':
                    Door(self, col, row)
                if tile == '!':
                    PowerUp(self, col, row)

    

    # defining run method
    def run(self):
        self.playing = True
        while self.playing: 
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    def quit(self):
        pg.quit()
        sys.exit()
    
    #continue to update so that things move; if this was not here the background would not be updated
    def update(self):
        self.all_sprites.update()
        self.countdown.ticking()

    #drawing game
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, "Coin count: " + str(self.player.money), 32, BLACK, 2, 2)
        self.draw_text(self.screen, "Heath: " + str(self.player.hp), 32, BLACK, 2, 4)
        pg.display.flip()

     


    # input method 
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if self.player.hp < 0:
                self.quit()
                # print("You died!")

                
    # draw text
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x*TILESIZE,y*TILESIZE)
        surface.blit(text_surface, text_rect)

    def show_start_screen(self):
        pass

g = Game()

# g.show_start_screen()
# running the function
while True:
    g.new()
    g.run()
    # g.show_go_screen()
