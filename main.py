'''
My final project is Flappy Fish. Flappy Fish is a spinoff of Flappy Bird, which is a single player 2D game. The objective is to avoid the pillars that can kill you and get the highest possible score. Each pillar past gives you 1 point.
'''

'''
Sources:
https://www.askpython.com/python/examples/flappy-bird-game-in-python
https://www.youtube.com/watch?v=rWtfClpWSb8
https://www.delftstack.com/howto/python-pygame/get_rect-pygame/
https://www.geeksforgeeks.org/python-time-time-method/
https://www.geeksforgeeks.org/python-datetime-timedelta-function/
https://www.youtube.com/watch?v=v_linpA7uXo
https://web.microsoftstream.com/video/b1bdbe8e-edc6-47a8-a2f9-c1aaf1b7930f
https://stackoverflow.com/questions/29885777/how-to-make-the-background-of-a-pygame-sprite-transparent#:~:text=from%20Tkinter%20import%20%2A%20import%20pygame%20from%20livewires,the%20program%20just%20as%20in%20tkinter%20games.screen.mainloop%20%28%29
https://stackoverflow.com/questions/35304498/what-are-the-pygame-surface-get-rect-key-arguments
my sister cropped the images on her ipad
https://www.pygame.org/docs/ref/mask.html#pygame.mask.from_surface
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
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (244, 255, 0)

# utility functions
# defines the function that visually draws text
def draw_text(text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

# set up asset folders here for importing images
introToProgrammingFinalProject_folder = os.path.dirname(__file__)
img_folder = os.path.join(introToProgrammingFinalProject_folder, 'images')

# init pygame and create a window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

# classes
class Game:
    def __init__(self):
        # initializes all imported pygame modules
        pg.init()
        # creates instance of pg.display and returns it
        self.display_surface = screen
        # displays title of game
        pg.display.set_caption('Flappy Fish')
        # time module/clock
        self.clock = clock
        self.active = True
        # create groups
        self.all_sprites = pg.sprite.Group() # all existing sprite
        self.collision_sprites = pg.sprite.Group() # floor, pipes, and fish (sprite that can be collided with)
        # scale factor by getting height of window and dividing it by height of background image file
        background_height = pg.image.load(os.path.join(img_folder, 'background.jpg')).convert_alpha().get_height()
        self.scale_factor = HEIGHT / background_height
        # sprite setup
        Background(self.all_sprites, self.scale_factor)
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor/ 2)
        self.fish = Fish(self.all_sprites, self.scale_factor / 25)
        # timer
        self.pipe_timer = pg.USEREVENT + 1
        pg.time.set_timer(self.pipe_timer, 1400)
        # game menu

    # collision method
    def collisions(self):
        hit = pg.sprite.spritecollide(self.fish, self.collision_sprites, False, pg.sprite.collide_mask)
        if hit:
            self.active = False
            self.fish.kill()

    # run method
    def run(self):
        previous_time = time.time()
        # while loop
        while True:
            # gets delta time, which is the time between the current and previous frame
            # it accounts for all framerates and makes it consistent by being multiplied by every movement in game
            delta_time = time.time() - previous_time
            previous_time = time.time()
            # event for loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                # setting different keys for jump mechanic
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.fish.jump()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.fish.jump()
                keys = pg.key.get_pressed()
                if keys[pg.K_w]:
                    self.fish.jump()
                if keys[pg.K_UP]:
                    self.fish.jump()
                if event.type == self.pipe_timer:
                    Pipe([self.all_sprites, self.collision_sprites], self.scale_factor / 4.9)
            # creates a time in seconds
            if self.active == True:
                ticks = pg.time.get_ticks()
                TIME = ticks / 1000

            # updating pygame
            self.display_surface.fill('black')
            self.clock.tick(FPS) # calling framrate
            self.all_sprites.update(delta_time) # updates sprites with delta time
            self.collisions()
            self.all_sprites.draw(self.display_surface) # draws sprites
            draw_text("TIME: " + str(TIME) + ' SECONDS', 22, WHITE, WIDTH / 2, HEIGHT / 24) # displays time
            pg.display.update()

class Background(Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        # loads background image
        background_image = pg.image.load(os.path.join(img_folder, 'Background.jpg')).convert_alpha()
        # gets height of original image and multiplies it by scale factor to get correct size to fit window
        done_height = background_image.get_height() * scale_factor
        # gets width of original image and multiplies it by scale factor to get correct size to fit window
        done_width = background_image.get_width() * scale_factor
        # transforms original image into fully sized image for background
        done_image = pg.transform.scale(background_image,(done_width, done_height))
        # create surface twice as wide as original background image to make double background for final image
        self.image = pg.Surface((done_width * 2, done_height))
        # draws fully sized image at (0,0)
        self.image.blit(done_image,(0,0))
        # draws fully sized image directly after fully sized image at (0,0) to create double background
        self.image.blit(done_image,(done_width,0))
        # sets top left as (0,0) and places fully sized image there
        self.rect = self.image.get_rect(topleft = (0,0))
        self.pos = pg.math.Vector2(self.rect.topleft)
    # update method
    def update(self, delta_time):
        # determines speed of camera movement
        self.pos.x -= 200 * delta_time
        # if centerx is less than 0, reset the positiion to centerx = 0
        if self.rect.centerx <= 0:
            self.pos.x = 0
        # rounds self.pos.x to whole numbers
        self.rect.x = self.pos.x

# similar to background sprite, but less complicated
class Ground(Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        # loads ground image
        ground_image = pg.image.load(os.path.join(img_folder, 'ground.png')).convert_alpha()
        # scales original ground image for final self.image
        self.image = pg.transform.scale(ground_image, pg.math.Vector2(ground_image.get_size()) * scale_factor)
        # draws fully sized image at (0,0)
        self.image.blit(self.image,(0,0))
        # draws fully sized image directly after fully sized image at (0,0) to create double ground
        self.image.blit(self.image,(0,WIDTH))
        # sets top left as (0,0) and places fully sized image there
        self.rect = self.image.get_rect(bottomleft = (0,HEIGHT))
        self.pos = pg.math.Vector2(self.rect.bottomleft)
        # gets rid of transparent pixels in image so they cannot touch the fish
        self.mask = pg.mask.from_surface(self.image)
    # update method
    def update(self, delta_time):
        # determines speed of camera movement
        self.pos.x -= 200 * delta_time
        # if centerx is less than 0, reset the positiion to centerx = 0
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = self.pos.x

class Pipe(Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        # loads pipe image
        pipe_image = pg.image.load(os.path.join(img_folder, 'pipe.png')).convert_alpha()
        # scales pipe image into final pipe image
        self.image = pg.transform.scale(pipe_image,pg.math.Vector2(pipe_image.get_size())* scale_factor)
        # x value is same for all pipes, but here, it chooses a random value to add to the x value to shift it some units to the left when it spawns
        x = WIDTH + randint(30,70)
        # chooses random element from sequence; in this case, it chooses whether the pipe is on the top or bottom
        placement = choice(('bottom', 'top'))
        # determines how far pipe sticks out when pipe is on the ground
        if placement == 'bottom':
            y = HEIGHT + randint(5,45)
            # places image on middle right bottom of screen
            self.rect = self.image.get_rect(midbottom = (x,y))
        # determines how far pipe sticks out when on top
        if placement == 'top':
            y = randint(-20, 0)
            # flips pipe vertically, but not horizontally
            self.image = pg.transform.flip(self.image, False, True)
            # places image on middle right top of screen
            self.rect = self.image.get_rect(midtop = (x,y))
        self.pos = pg.math.Vector2(self.rect.topleft)
        # gets rid of transparent pixels in image so they cannot touch fish
        self.mask = pg.mask.from_surface(self.image)
    # update method
    def update(self, delta_time):
        # speed of pipes
        self.pos.x -= 200 * delta_time
        self.rect.x = self.pos.x 
        # if pipe goes 200 units to the left of screen, delete it
        if self.rect.right <= -200:
            self.kill()

class Fish(Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        # loads fish image
        fish_image = pg.image.load(os.path.join(img_folder, 'fish.png')).convert_alpha()
        # scales fish image
        scaled_image = pg.transform.scale(fish_image,pg.math.Vector2(fish_image.get_size())* scale_factor)
        self.image = scaled_image
        # makes starting position of image at midleft point by dividing width by 20 and height by 2 to get coordinates
        self.rect = self.image.get_rect(midleft = (WIDTH / 20, HEIGHT / 2))
        self.pos = pg.math.Vector2(self.rect.topleft)
        # gravity and velocity
        self.gravity = 700
        self.direction = 0
        # gets rid of transparent pixels in image so they cannot touch the ground or pipes
        self.mask = pg.mask.from_surface(self.image)
    # method for gravity
    def grav(self, delta_time):
        self.direction += self.gravity * delta_time
        self.pos.y += self.direction * delta_time
        self.rect.y = self.pos.y
    # method for jump mechanic
    def jump(self):
        self.direction = -300
    # update method
    def update(self, delta_time):
        # create methods with delta time for movement
        self.grav(delta_time)
        # creates ceiling by resetting y-coordinate to 0 whenever it is 0 or less than that
        if self.rect.y <= 0:
            self.pos.y = 0

# makes while loop always run
running = True
# runs game class by creating instance of game class and calling it through run()
while running:
    game = Game()
    game.run()