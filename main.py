'''
My final project is Flappy Fish. Flappy Fish is a spinoff of Flappy Bird, which is a single player 2D game. The objective is to avoid the pillars that can kill you and get the highest possible score. Each pillar past gives you 1 point.
'''

'''
Sources:
https://www.askpython.com/python/examples/flappy-bird-game-in-python
https://www.geeksforgeeks.org/python-datetime-timedelta-function/
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
    def __init__(self, groups,scale_factor):
        super().__init__(groups)
        background_image = pg.image.load(os.path.join(img_folder, 'Background.jpg')).convert()
        # gets height of original image and multiplies it by scale factor to get correct size to fit window
        done_height = background_image.get_height() * scale_factor
        # gets width of original image and multiplies it by scale factor to get correct size to fit window
        done_width = background_image.get_width() * scale_factor
        # # fully sized image to be created twice
        done_image = pg.transform.scale(background_image,(done_width, done_height))

        # create surface twice as wide as original background image to make double background
        self.image = pg.Surface((done_width * 2, done_height))
        self.image.blit(done_image,(0,0))
        self.image.blit(done_image,(done_width,0))

        self.rect = self.image.get_rect(topleft = (0,0))
        self.pos = pg.math.Vector2(self.rect.topleft)

    def update(self, delta_time):
        self.pos.x -= 200 * delta_time
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
        background_height = pg.image.load(os.path.join(img_folder, 'Background.jpg')).convert().get_height()
        self.scale_factor = HEIGHT / background_height

        # sprite setup
        Background(self.all_sprites, self.scale_factor)
    
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
            self.all_sprites.update(delta_time)
            self.all_sprites.draw(self.display_surface)
            pg.display.update()
            self.clock.tick(FPS)
running = True
while running:
    game = Game()
    game.run()