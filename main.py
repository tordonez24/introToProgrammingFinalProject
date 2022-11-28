'''
My final project is Flappy Fish. Flappy Fish is a spinoff of Flappy Bird, which is a single player 2D game. The objective is to avoid the pillars that can kill you and get the highest possible score. Each pillar past gives you 1 point.
'''

'''
Sources:
https://www.askpython.com/python/examples/flappy-bird-game-in-python
'''

# imported libraries
import pygame as pg
import sys
import time

# built in libraries
import random

# created libraries
from settings import *
import os

# global variables

# utility functions

# init pygame and create a window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game...")
clock = pg.time.Clock()

# classes

# Game loop
running = True
if running == True:
    # keep the loop running using clock
    clock.tick(FPS)