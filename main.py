'''
My final project is Flappy Fish. Flappy Fish is a spinoff of Flappy Bird, which is a single player 2D game. The objective is to avoid the pillars that can kill you and get the highest possible score. Each pillar past gives you 1 point.
'''

'''
Sources:
https://www.askpython.com/python/examples/flappy-bird-game-in-python
https://www.geeksforgeeks.org/python-datetime-timedelta-function/
https://www.delftstack.com/howto/python-pygame/get_rect-pygame/
'''

# imported libraries
import pygame as pg
from pygame.sprite import Sprite
import sys
import time

# built in libraries
import random
from random import choice, randint
import os

# created libraries
from settings import *

# global variables

# utility functions

# set up asset folders here
introToProgrammingFinalProject_folder = os.path.dirname(__file__)
img_folder = os.path.join(introToProgrammingFinalProject_folder, 'images')

# init pygame and create a window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game...")
clock = pg.time.Clock()

# classes

class Background(Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        # loads background image
        background_image = pg.image.load(os.path.join(img_folder, 'Background.jpg')).convert() 
        # gets height of original image and multiplies it by scale factor to get correct size to fit window
        done_height = background_image.get_height() * scale_factor
        # gets width of original image and multiplies it by scale factor to get correct size to fit window
        done_width = background_image.get_width() * scale_factor
        # transforms original image into fully sized image for background
        done_image = pg.transform.scale(background_image,(done_width, done_height))
        # create surface twice as wide as original background image to make double background
        self.image = pg.Surface((done_width * 2, done_height))
        # draws fully sized image at (0,0)
        self.image.blit(done_image,(0,0))
        # draws fully sized image directly after fully sized image at (0,0) to create double background
        self.image.blit(done_image,(done_width,0))
        # sets top left as (0,0) and places fullysized image there
        self.rect = self.image.get_rect(topleft = (0,0))
        self.pos = pg.math.Vector2(self.rect.topleft)

    def update(self, delta_time):
        # determines speed of camera movement
        self.pos.x -= 200 * delta_time
        # if centerx is less than 0, reset the positiion to centerx = 0
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)

class Ground(Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        # loads ground image
        ground_image = pg.image.load(os.path.join(img_folder, 'ground.png')).convert() 
        # gets height of original image and multiplies it by scale factor to get correct size to fit window
        done1_height = ground_image.get_height() * scale_factor
        # gets width of original image and multiplies it by scale factor to get correct size to fit window
        done1_width = ground_image.get_width() * scale_factor
        # transforms original image into fully sized image for background
        done1_image = pg.transform.scale(ground_image,(done1_width, done1_height))
        # create surface twice as wide as original background image to make double background
        self.image = pg.Surface((done1_width * 2, done1_height))
        # draws fully sized image at (0,0)
        self.image.blit(done1_image,(0,0))
        # draws fully sized image directly after fully sized image at (0,0) to create double background
        self.image.blit(done1_image,(done1_width,0))
        # sets top left as (0,0) and places fully sized image there
        self.rect = self.image.get_rect(bottomleft = (0,HEIGHT))
        self.pos = pg.math.Vector2(self.rect.bottomleft)

    def update(self, delta_time):
        # determines speed of camera movement
        self.pos.x -= 200 * delta_time
        # if centerx is less than 0, reset the positiion to centerx = 0
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)

class Game:
    def __init__(self):
        # initializes all imported pygame modules
        pg.init()
        # creates instance of pg.display and returns it
        self.display_surface = pg.display.set_mode((WIDTH,HEIGHT))
        # displays title of game
        pg.display.set_caption('Flappy Fish')
        # time module/clock
        self.clock = pg.time.Clock()

        # create groups
        self.all_sprites = pg.sprite.Group() # all existing sprite
        self.collision_sprite = pg.sprite.Group() # floor and pipes (sprite that can be collided with)

        # scale factor
        background_height = pg.image.load(os.path.join(img_folder, 'background.jpg')).convert().get_height()
        self.scale_factor = HEIGHT / background_height

        # sprite setup
        Background(self.all_sprites, self.scale_factor)
        Ground(self.all_sprites, self.scale_factor)
    
    def run(self):
        last_time = time.time()
        # while loop
        while True:
            # delta time which accounts for different framrates
            delta_time = time.time() - last_time
            last_time = time.time()
            # event for loop which quits the game when told to
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            # updating pygame and calling the framrate
            self.display_surface.fill('black')
            self.all_sprites.update(delta_time) # updates sprites with delta time
            self.all_sprites.draw(self.display_surface) # draws sprites
            pg.display.update()
            self.clock.tick(FPS)
# makes while loop always run
running = True
# runs game class by creating instance of game class and calling it through run()
while running:
    game = Game()
    game.run()