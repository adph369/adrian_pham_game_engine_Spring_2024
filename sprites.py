# This file was created by Adrian Pham

# import necessary libraries
import pygame as pg
from pygame.sprite import Sprite
from settings import *
from random import choice
from clock import * 

# create a player class
class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.money = 0
        self.hp = 100
        self.speed = PLAYER_SPEED
        self.gamelevel = 1
        self.cooling = False
        self.status = ""
    # Character position
    # def move(self, dx = 0, dy = 0):
    #     self.x += dx
    #     self.y += dy
    
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed 
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed  
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed
        # calculating to reduce speed for diagonal movement, sqrt(2)/2. YAY MATH!
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    # wall collisions; horizontally based
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right 
                self.vx = 0 
                self.rect.x = self.x

    # wall collisions; vertically based
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0 
                self.rect.y = self.y
    # collisions with any type of object: type of object, remove or not when collide
    def collide_with_obj(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.money += 1
            if str(hits[0].__class__.__name__) == "PowerUp":
                self.game.countdown.cd = 5
                self.cooling = True
                # self.vx, self.vy = 500, 500
                self.status = "Invincible"
            if str(hits[0].__class__.__name__) == "Enemy":
                if self.status == "Invincible":
                    self.hp += 0
                if self.status != "Invincible":
                    self.hp -= 3
            if str(hits[0].__class__.__name__) == "Chaser":
                if self.status == "Invincible":
                    self.hp += 0
                if self.status != "Invincible":
                    self.hp -= 2
            if str(hits[0].__class__.__name__) == "Door":
                self.gamelevel += 1

        
    def update(self):
        # self.rect.x = self.x * TILESIZE
        # self.rect.y = self.y * TILESIZE
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.collide_with_obj(self.game.coins, True)
        self.collide_with_obj(self.game.enemies, False)
        self.collide_with_obj(self.game.powerups, True)
        if self.game.countdown.cd < 1:
            self.cooling = False
        if not self.cooling:
            # self.vx, self.vy = PLAYER_SPEED, PLAYER_SPEED
            self.status = ""

    

# create a wall class
class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Coin(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Enemy(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemies
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.vx, self.vy = ENEMY_SPEED, ENEMY_SPEED
        self.speed = 1
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
    # def increase_difficulty(self):
    #     if Player.money > 2:
    #         self.vx, self.vy = ENEMY_SPEED + 300, ENEMY_SPEED + 300


    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right 
                self.vx = -self.vx
                self.rect.x = self.x
    # wall collisions; vertically based
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = -self.vy
                self.rect.y = self.y

    def update(self):
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')

class Chaser(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemies
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHTRED)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.vx, self.vy = ENEMY_SPEED, ENEMY_SPEED
        self.speed = 1
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right 
                self.vx = 0
                self.rect.x = self.x
    # wall collisions; vertically based
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def update(self):
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt

        if self.rect.x < self.game.player.rect.x:
            self.vx = ENEMY_SPEED
        if self.rect.x > self.game.player.rect.x:
            self.vx = -ENEMY_SPEED    
        if self.rect.y < self.game.player.rect.y:
            self.vy = ENEMY_SPEED
        if self.rect.y > self.game.player.rect.y:
            self.vy = -ENEMY_SPEED
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')

class Door(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.door
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class PowerUp(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.powerups
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE



