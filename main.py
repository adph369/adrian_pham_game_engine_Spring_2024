# This file was created by: Adrian Pham
# added hp bar, game levels, power-ups

# importing necessary libaries
import pygame as pg  
from settings import *
from sprites import *
from clock import *
import sys
from random import randint
from os import path 
from math import floor

# print(pg.font.get_fonts())

# creating game class
class Game:
    # initializes all code in a class
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500,100)
        self.gamestage = "start"
        self.load_data()
        self.money = 0
        self.cooling = False

    # load data: images and map
    def load_data(self):
        self.gamelevel = 1
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        map_folder = path.join(game_folder, 'maps')
        self.player_img = pg.image.load(path.join(img_folder, 'man.png')).convert_alpha()
        self.coin_img = pg.image.load(path.join(img_folder, 'coin.png')).convert_alpha()
        self.map_data = []
        with open(path.join(map_folder, 'map' + str(self.gamelevel) + '.txt'), 'rt') as f:
            for line in f:
                # print(line)
                self.map_data.append(line)
    
    # change level maps
    def change_map(self):
        game_folder = path.dirname(__file__)
        map_folder = path.join(game_folder, 'maps')
        if self.player.changelevel == True:
            # kills all sprites so that new level does not contain sprites from old level
            for s in self.all_sprites:
                s.kill()
            # sets to false so that the level doesn't keep running
            self.player.changelevel = False
            self.gamelevel += 1
            self.map_data = []
            with open(path.join(map_folder, 'map' + str(self.gamelevel) + '.txt'), 'rt') as f:
                for line in f:
                    self.map_data.append(line)
            for row, tiles in enumerate(self.map_data):
                for col, tile in enumerate(tiles):
                    if tile == '1':
                        Wall(self, col, row)
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
                        
    def new(self):
        # initialize all variables, setup groups, instantiate classes
        print("Create new game...")
        self.countdown = Timer(self)
        self.all_sprites = pg.sprite.Group()
        self.health = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        # drawing the game map
        for row, tiles in enumerate(self.map_data):
            # enumerate: assign numbers to elements in a list
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
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
    # defining run method - what happens while playing
    def run(self):
        self.playing = True
        while self.playing: 
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            # shows which screen based on conditions
            if self.gamestage == "start":
                self.show_start_screen()
            if self.gamestage == "playing":
                self.update()
                self.draw()
            if self.gamestage == "death":
                self.game_over()
            # print(self.gamelevel)

    # quit method
    def quit(self):
        pg.quit()
        sys.exit()
    
    #continue to update so that things move; if this was not here the background, timer, and map would not be updated
    def update(self):
        self.all_sprites.update()
        self.countdown.ticking()
        self.change_map()

    # draw grid
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    # input method
    def events(self):
        for event in pg.event.get():
            # if press X, quit game
            if event.type == pg.QUIT:
                self.quit()
            # if hp < 0, set hp to 100 so that it doesn't keep dying, and show death screen
            if self.player.hp < 0:
                # self.quit()
                self.player.hp = 100
                self.gamestage = "death"
                # print("You died!")

                
    # draw text
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('pristina')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x * TILESIZE, y * TILESIZE)
        surface.blit(text_surface, text_rect)

    # draw health bar
    def draw_health_bar(game, surface, x, y, hp):
        BAR_LENGTH = 10
        BAR_HEIGHT = 5
        if hp < 0:
            hp = 0
        fill = (hp / 100 * 3.3) * BAR_LENGTH
        fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
        # as hp decreases, bar color changes
        pg.draw.rect(surface, GREEN, fill_rect)
        if hp < 50:
            pg.draw.rect(surface, ORANGE, fill_rect)
        if hp < 25:
            pg.draw.rect(surface, RED, fill_rect)

    def draw(self):
        # self.screen.fill(BLACK)
        # if self.gamestage != "game over":
            self.screen.fill(BGCOLOR)
            # draws the grid to show squares, unnecessary so removed to look nicer
            # self.draw_grid()
            self.all_sprites.draw(self.screen)
            # different positions of the text for every level to prevent overlap :(
            if self.gamelevel == 1:
                self.draw_text(self.screen, "Coin count: " + str(self.money), 40, BLACK, 1.25, 1.25)
            if self.gamelevel == 2:
                self.draw_text(self.screen, "Coin count: " + str(self.money), 40, BLACK, 3.5, 1.25)
            if self.gamelevel == 3:
                self.draw_text(self.screen, "Coin count: " + str(self.money), 40, BLACK, 13, 20)
            if self.gamelevel == 4:
                self.draw_text(self.screen, "Coin count: " + str(self.money), 40, BLACK, 1.25, 1.25)
            # self.draw_text(self.screen, "Health: " + str(self.player.hp), 32, WHITE, 2, 4)
            self.draw_health_bar(self.screen, self.player.x, self.player.y + 32, self.player.hp)
            if self.player.status != "":
                if self.gamelevel == 1:
                    self.draw_text(self.screen, "You are " + str(self.player.status) + " for 5 seconds!", 30, BLACK, 1.25, 21)
                if self.gamelevel == 2:
                    self.draw_text(self.screen, "You are " + str(self.player.status) + " for 5 seconds!", 25, BLACK, 21.5, 1.25)
                if self.gamelevel ==3:
                    self.draw_text(self.screen, "You are " + str(self.player.status) + " for 5 seconds!", 25, BLACK, 11.5, 21.5)
                if self.gamelevel == 4:
                    self.draw_text(self.screen, "You are " + str(self.player.status) + " for 5 seconds!", 30, BLACK, 2.5, 21)
            pg.display.flip()

    # show the start screen, if space pressed start playing
    def show_start_screen(self):
        self.screen.fill(LIGHTGREEN)
        keys = pg.key.get_pressed()
        self.draw_text(self.screen, "Welcome to That Game!", 90, BLACK, 5, 7.5)
        self.draw_text(self.screen, "Press space to start!", 60, BLACK, 10, 15)
        if keys[pg.K_SPACE]:
            self.gamestage = "playing"
        pg.display.flip()
        self.run()
        
    # game over screen
    def game_over(self):
        self.screen.fill(BLACK)
        for s in self.all_sprites:
            s.kill()
        # self.player.hp = 100
        self.draw_text(self.screen, "Game Over! :(", 60, WHITE, 12, 15)
        self.countdown.cd = 5
        if self.countdown.cd > 2 and self.countdown.cd < 2.1:
            self.cooling = True
        if self.cooling == True:
            self.quit()
        # self.draw_text(self.screen, "Press R to restart!", 60, WHITE, 10, 15)
        # keys = pg.key.get_pressed()
        # if keys[pg.K_r]:
        #     self.gamestage = "start"
        pg.display.flip()

g = Game()

# running the function
while True:
    g.new()
    g.run()