# This file was created by Adrian Pham

# import necessary libraries
import pygame as pg
from pygame.sprite import Sprite
from settings import *
from random import choice
from clock import * 
from os import path

game_folder = path.dirname(__file__)
image_folder = path.join(game_folder, 'images')

SPRITESHEET = "manmove.png"
class Spritesheet:
    def __init__(self, filename):
        # utility class for loading and parsing spritesheets
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width, height))
        # image = pg.transform.scale(image, (width * 4, height * 4))
        return image

# create a player class
class Player(Sprite):
    # initialize the class, create its attributes
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = game.player_img
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.spritesheet = Spritesheet(path.join(image_folder, SPRITESHEET))
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.hp = 100
        self.speed = PLAYER_SPEED
        self.changelevel = False
        self.cooling = False
        self.status = ""
        self.current_frame = 0
        self.last_update = 0 
        self.material = True
        self.jumping = False
        self.walking = False        

    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0, 0, 32, 32), self.spritesheet.get_image(32, 0, 32, 32)]
        self.walking_frames = [self.spritesheet.get_image(0, 0, 32, 32), self.spritesheet.get_image(32, 0, 32, 32)]
    
    
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            if not self.walking:
                self.image = self.standing_frames[self.current_frame]
            else:
                self.image = self.walking_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom 

    
    # movement based on WASD/arrow keys
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
                self.game.money += 1
            # timed power-ups
            if str(hits[0].__class__.__name__) == "PowerUp":
                self.game.countdown.cd = 5
                self.cooling = True
                self.status = choice(POWER_UP_TYPES)
            # if invincible, no dmg taken
            if str(hits[0].__class__.__name__) == "Enemy":
                if self.status == "invincible":
                    self.hp += 0
                if self.status != "invincible":
                    self.hp -= 3
            if str(hits[0].__class__.__name__) == "Chaser":
                if self.status == "invincible":
                    self.hp += 0
                if self.status != "invincible":
                    self.hp -= 2
            if str(hits[0].__class__.__name__) == "Door":
                self.changelevel = True
    
    # constantly updates player position and movement
    def update(self):
        self.animate()
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        # activate collisions
        self.collide_with_obj(self.game.coins, True)
        self.collide_with_obj(self.game.enemies, False)
        self.collide_with_obj(self.game.powerups, True)
        self.collide_with_obj(self.game.doors, False)
        # power-up timer
        if self.game.countdown.cd < 1:
            self.cooling = False
        if not self.cooling:
            self.status = ""
            self.speed = 300
        if self.status == "speedy":
            self.speed = 500
        
    

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

# coin class
class Coin(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.coin_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# enemy class
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

    # wall collisions; horizontally based
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
    
    # constantly updates position, speed, collisions
    def update(self):
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')

# chaser (type of enemy) class
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

    # constantly updates motion and position
    def update(self):
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt

        # if chaser coordinates are not same as player's move until they are
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

# create door class
class Door(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.doors
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# create power-up class
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

class Shop(Sprite):
    def __init__(self, game):
        self.game = game 
        self.visible = False
        self.width = 260
        self.height = 160
        self.color = TRANSPARENT_BEIGE
        self.x = 50
        self.y = 550
        # self.menu_surface = pg.Surface((self.width, self.height))
        self.menu_surface = pg.Surface((self.width, self.height), flags=pg.SRCALPHA)
        self.menu_surface.fill(TRANSPARENT_BEIGE)

    def draw_menu(self, screen):
        if self.visible:
            self.menu_surface.fill(TRANSPARENT_BEIGE)
            pg.draw.rect(self.menu_surface, self.color, (self.x, self.y, TILESIZE * 8, TILESIZE * 5))
            screen.blit(self.menu_surface, (self.x, self.y))

    def toggle_visibility(self):
        self.visible = not self.visible

# done with help from ChatGPT
class Button:
    def __init__(self, game, text, position, size, color, hover_color, action = None, clickable = True):
        self.game = game
        self.text = text
        self.position = position
        self.size = size
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.font = pg.font.Font(None, 32)  # Font for button text
        self.hovered = False
        self.clickable = clickable

    def draw(self, screen):
        
        clickable = self.is_clickable()
        # Create a button rectangle at the specified position and size
        button_rect = pg.Rect(self.position, self.size)

        # Change button color when hovered
        if self.hovered and self.clickable:
            color = self.hover_color
        else:
            color = self.color

        # Draw button rectangle
        pg.draw.rect(screen, color, button_rect)

        # Render button text
        text_surface = self.font.render(self.text, True, pg.Color('white'))
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if self.clickable:
            if event.type == pg.MOUSEMOTION:
                # Check if mouse is hovering over the button
                self.hovered = self.is_hovered(event.pos)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if self.hovered and self.action:
                    # Execute button action if clicked
                    self.action()

    def is_hovered(self, mouse_pos):
        # Check if mouse position is within button bounds
        button_rect = pg.Rect(self.position, self.size)
        return button_rect.collidepoint(mouse_pos)

    def set_clickable(self, clickable):
        self.clickable = clickable 

    def is_clickable(self):
        if self.game.money >= 5:
            self.set_clickable(True)
        else:
            self.set_clickable(False)      
