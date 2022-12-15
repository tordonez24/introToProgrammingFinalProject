'''
Tyler Ordonez
My final project is Flappy Fish. Flappy Fish is a spinoff of Flappy Bird, which is a single player 2D game. The objective is to avoid the pillars that can kill you and get the longest time alive and the most stars.
'''

'''
Sources:
https://www.askpython.com/python/examples/flappy-bird-game-in-python
https://www.youtube.com/watch?v=rWtfClpWSb8
https://www.delftstack.com/howto/python-pygame/get_rect-pygame/
https://www.geeksforgeeks.org/python-time-time-method/
https://www.youtube.com/watch?v=v_linpA7uXo
https://www.youtube.com/watch?v=VUFvY349ess&t=17s
https://web.microsoftstream.com/video/b1bdbe8e-edc6-47a8-a2f9-c1aaf1b7930f
https://stackoverflow.com/questions/29885777/how-to-make-the-background-of-a-pygame-sprite-transparent#:~:text=from%20Tkinter%20import%20%2A%20import%20pygame%20from%20livewires,the%20program%20just%20as%20in%20tkinter%20games.screen.mainloop%20%28%29
https://stackoverflow.com/questions/35304498/what-are-the-pygame-surface-get-rect-key-arguments
my sister cropped the images on her ipad
https://www.pygame.org/docs/ref/mask.html#pygame.mask.from_surface
my friend who knows pygame and python in general
'''

# imported libraries
# programming language library for making applications like games
import pygame as pg
from pygame.sprite import Sprite

# built in libraries
from random import * # used to generate pseudo-random variables; EX: generate random numbers, choose single option from multiple options
import sys # provides functions and variables that are used to change different parts of runtime environment
import time # allows to work with time in Python; EX: getting current time, pausing the program
import os # provides functions for interacting with the operating system

# created libraries
from settings import * # contains height and width of window, time, and FPS variables; the * imports everything from it

# global variables for colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (244, 255, 0)

# defines the function that visually draws text (from game we made in class)
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
        # creates screen
        self.display_surface = screen
        # displays title of game
        pg.display.set_caption('Flappy Fish')
        # create groups
        self.all_sprites = pg.sprite.Group() # all existing sprites
        self.collision_sprites = pg.sprite.Group() # pipe collision
        self.g_collision_sprites = pg.sprite.Group() # ground collision
        self.star_collision_sprites = pg.sprite.Group() # star collision
        self.pwr_collision_sprites = pg.sprite.Group() # extra life collision
        # creates scale factor by getting height of window and dividing it by height of background image file
        back_height = pg.image.load(os.path.join(img_folder, 'background.jpg')).convert_alpha().get_height()
        self.sf = HEIGHT / back_height
        # timer
        self.pipe_timer = pg.USEREVENT + 1
        pg.time.set_timer(self.pipe_timer, 1400)
        # part of resetting timer, lives, and stars when playing again after death
        self.restart = 0
        self.star_restart = 0
        # time module/clock
        self.clock = clock
        # living status
        self.alive = True
        # instantiate classes
        self.back = Back(self.all_sprites, self.sf / 1.72)
        self.ground = Ground([self.all_sprites, self.g_collision_sprites], self.sf/ 2)
        self.player = Player(self.all_sprites, self.sf / 25)
        # loads play again image
        self.pagain_surface = pg.image.load(os.path.join(img_folder, 'pagain.png')).convert_alpha()
        # play again image's coordinatess are established
        self.pagain_rect = self.pagain_surface.get_rect(center = (WIDTH / 2, HEIGHT / 3.5))
        # variable for # of initial stars
        self.stars = 0
        # variable for # of initial lives
        self.life = 1
    # collision method
    def collisions(self, delta_time):
        if self.life > 0:
            # if player has lives and hits a pipe, the pipe is broken and 1 life is lost
            pipe_hit = pg.sprite.spritecollide(self.player, self.collision_sprites, True, pg.sprite.collide_mask)
            if pipe_hit:
                self.life -= 1
            # if player has lives and hits the ground, the player is teleported back to centermiddle and only 1 life is lost
            ground_hit = pg.sprite.spritecollide(self.player, self.g_collision_sprites, False, pg.sprite.collide_mask)
            if ground_hit:
                self.player.pos.y = HEIGHT / 2
                self.player.vel = 0
                self.life -= 1
        # if lives are 0 or negative, resets lives to 0, deletes player sprite, and set alive status to False
        if self.life <= 0:
            self.life = 0
            self.alive = False
            self.player.kill()
        # if player is dead, display play again screen and kill all sprites execept for ground and background
        if self.alive == False:
            self.display_surface.blit(self.pagain_surface, self.pagain_rect)
            for sprite in self.collision_sprites.sprites():
                sprite.kill()
            for sprite in self.star_collision_sprites.sprites():
                sprite.kill()
            for sprite in self.pwr_collision_sprites.sprites():
                sprite.kill()
            # stops movement of ground and background
            self.back.pos.x += 150 * delta_time
            self.ground.pos.x += 200 * delta_time
    # method for star collisions
    def star_collisions(self):
        # if it hits, the star is deleted and 1 star is added to counter
        hit = pg.sprite.spritecollide(self.player, self.star_collision_sprites, True)
        if hit:
            self.stars += 1
    # method for heart collisions
    def pwr_collisions(self):
        # if it hits, the heart is deleted and 1 extra life is added to counter
        hit = pg.sprite.spritecollide(self.player, self.pwr_collision_sprites, True)
        if hit:
            self.life +=1
    # run method
    def run(self):
        p_time = time.time()
        running = True
        # while loop
        while running:
            # creates delta time, which is the time between the current and previous frame (https://www.youtube.com/watch?v=rWtfClpWSb8)
            # it accounts for all framerates and makes it consistent by being multiplied by every movement in game
            delta_time = time.time() - p_time
            p_time = time.time()
            # creates a time in seconds
            # when player is alive...
            if self.alive == True:
                ticks = (pg.time.get_ticks() - self.restart)
                TIME = ticks / 1000
                stars = self.stars- self.star_restart
            # event for loop
            for event in pg.event.get():
                # setting different keys for jump mechanic
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.player.jump()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.player.jump()
                keys = pg.key.get_pressed()
                if keys[pg.K_w]:
                    self.player.jump()
                if keys[pg.K_UP]:
                    self.player.jump()
                # when player is alive and timer is going...
                if event.type == self.pipe_timer and self.alive:
                    Pipe([self.all_sprites, self.collision_sprites], self.sf / 4.9)
                    chance = randint(1,2)
                    if chance == 1: # 50% chance to spawn a star somewhere on the screen
                        Star([self.all_sprites, self.star_collision_sprites], self.sf / 10)
                    chance1 = randint(1,12) # 8% chance to spawn an extra life in middle of screen
                    if chance1 == 1:
                        Pwrup([self.all_sprites, self.pwr_collision_sprites], self.sf / 17)
                # while alive and playing game, nothing will happen; while not playing, dead, and on "play again" screen, pressing "y" will respawn the player and reset the time, lives, and stars
                if keys[pg.K_y]:
                    if self.alive == True:
                        pass
                    if self.alive == False:
                        self.player = Player(self.all_sprites, self.sf / 25)
                        self.alive = True
                        self.life = 1
                        self.restart = pg.time.get_ticks()
                        self.star_restart = self.stars
                # while playing game, nothing will happen; while dead, if player presses "n" key on play again screen, window closes and everything quits
                if keys[pg.K_n]:
                    if self.alive == True:
                        pass
                    if self.alive == False:
                        pg.quit()
                        sys.exit()
                # if window is closed, everything quits
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            # updating pygame
            self.clock.tick(FPS) # calling framrate
            self.all_sprites.update(delta_time) # updates sprites through delta time
            self.all_sprites.draw(self.display_surface) # draws sprites
            self.collisions(delta_time)
            self.star_collisions()
            self.pwr_collisions()
            draw_text("TIME: " + str(TIME) + ' SECONDS', 22, BLACK, WIDTH / 2, HEIGHT / 24) # displays time (from pygame assignment)
            draw_text("STARS: " + str(stars), 22, BLACK, WIDTH / 2, HEIGHT / 14)
            draw_text("LIVES: " + str(self.life), 22, BLACK, WIDTH / 2, HEIGHT / 10)
            draw_text("FPS: " + str(self.clock.tick(FPS)), 22, BLACK, WIDTH - 80, HEIGHT / 24)
            pg.display.update()

# regular sprite with jump mechanic and gravity
class Player(Sprite):
    def __init__(self, groups, sf):
        super().__init__(groups)
        # loads player image
        player_image = pg.image.load(os.path.join(img_folder, 'fish.png')).convert_alpha()
        # scales player image
        scaled_image = pg.transform.scale(player_image,pg.math.Vector2(player_image.get_size())* sf)
        self.image = scaled_image
        # makes starting position of image at midleft point by dividing width by 20 and height by 2 to get coordinates
        self.rect = self.image.get_rect(midleft = (WIDTH / 20, HEIGHT / 2))
        self.pos = pg.math.Vector2(self.rect.topleft)
        # gets rid of transparent pixels in image so they cannot touch the ground or pipes
        self.mask = pg.mask.from_surface(self.image)
        # gravity and velocity
        self.gravity = 700
        self.vel = 0
    # method for jump mechanic
    def jump(self):
        self.vel = -300
    # update method
    def update(self, delta_time):
        # gravity
        self.vel += self.gravity * delta_time
        self.pos.y += self.vel * delta_time
        self.rect.y = self.pos.y
        # creates ceiling by resetting y-coordinate to 0 whenever it is 0 or less than that
        if self.rect.y <= 0:
            self.pos.y = 0
        # creates floor by resetting y-coordinate to 850 whenever it is 850 or higher
        if self.rect.y >= 850:
            self.pos.y = 850

class Back(Sprite):
    def __init__(self, groups, sf):
        super().__init__(groups)
        # loads background image
        back_image = pg.image.load(os.path.join(img_folder, 'background.png')).convert_alpha()
        self.width = back_image.get_width() * sf
        # scales original ground image for final self.image
        self.image = pg.transform.scale(back_image, pg.math.Vector2(back_image.get_size()) * sf)
        self.image.blit(self.image,(0,0))
        # sets bottom left as (0,height) and puts image there
        self.rect = self.image.get_rect(bottomleft = (0,HEIGHT))
        self.pos = pg.math.Vector2(self.rect.bottomleft)
    # update method
    def update(self, delta_time):
        # determines speed of background movement
        self.pos.x -= 150 * delta_time
        # if centerx is less than 0, reset the positiion to x = 0
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = self.pos.x

# similar to background sprite
class Ground(Sprite):
    def __init__(self, groups, sf):
        super().__init__(groups)
        # loads ground image
        ground_image = pg.image.load(os.path.join(img_folder, 'ground.png')).convert_alpha()
        # scales original ground image for final self.image
        self.image = pg.transform.scale(ground_image, pg.math.Vector2(ground_image.get_size()) * sf)
        # creates double ground
        self.image.blit(self.image,(0,0))
        self.image.blit(self.image,(0,WIDTH))
        # sets bottom left as (0,height) and puts image there
        self.rect = self.image.get_rect(bottomleft = (0,HEIGHT))
        self.pos = pg.math.Vector2(self.rect.bottomleft)
        # gets rid of transparent pixels in image so they cannot touch the player
        self.mask = pg.mask.from_surface(self.image)
    # update method
    def update(self, delta_time):
        # determines speed of ground movement
        self.pos.x -= 200 * delta_time
        # if centerx is less than 0, reset the position to x = 0
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = self.pos.x

# basic moving sprite
class Star(Sprite):
    def __init__(self, groups, sf):
        super().__init__(groups)
        x = WIDTH
        y = HEIGHT- randint (50,800) # can spawn at any height on visible screen
        star_image = pg.image.load(os.path.join(img_folder, 'star.png')).convert_alpha() # loads image of star
        self.image = pg.transform.scale(star_image,pg.math.Vector2(star_image.get_size())* sf) # scales star
        # sets x,y as center and draws image there
        self.rect = self.image.get_rect(center = (x,y))
        self.pos = pg.math.Vector2(self.rect.center)
        # gets rid of transparent pixels in image so they cannot touch the player
        self.mask = pg.mask.from_surface(self.image)
    def update(self, delta_time):
        # speed of star
        self.pos.x -= 200 * delta_time
        self.rect.x = self.pos.x
        # if it goes 200 units to the left, kill
        if self.rect.x <= -200:
            self.kill()

# almost exact same as star sprite, except this one can only spawn in the center row of the window where no pipes are
class Pwrup(Sprite):
    def __init__(self, groups, sf):
        super().__init__(groups)
        # cords so it spawns in right center of screen
        x = WIDTH
        y = HEIGHT / 2
        star_image = pg.image.load(os.path.join(img_folder, 'heart.png')).convert_alpha() # loads image
        self.image = pg.transform.scale(star_image,pg.math.Vector2(star_image.get_size())* sf) # scales image
        # sets x,y as center and draws image there
        self.rect = self.image.get_rect(center = (x,y))
        self.pos = pg.math.Vector2(self.rect.center)
        # gets rid of transparent pixels in image so they cannot touch the player
        self.mask = pg.mask.from_surface(self.image)
    def update(self, delta_time):
        # speed of heart powerup
        self.pos.x -= 200 * delta_time
        self.rect.x = self.pos.x
        # if it goes 200 units to the left, kill
        if self.rect.x <= -200:
            self.kill()

# pretty much the exact same thing as powerup and star sprites, except it has a 50% chance to be flipped and placed on ceiling
class Pipe(Sprite):
    def __init__(self, groups, sf):
        super().__init__(groups)
         # x value is same for all pipes, but here, it chooses a random value to add to the x value to shift it some units to the left when it spawns
        x = WIDTH + randint(30,70)
        # loads pipe image
        pipe_image = pg.image.load(os.path.join(img_folder, 'pipe.png')).convert_alpha()
        # scales pipe image into final pipe image
        self.image = pg.transform.scale(pipe_image,pg.math.Vector2(pipe_image.get_size())* sf)
        # chooses random element from sequence; in this case, it chooses whether the pipe is on the top or bottom
        placement = randint(1,2)
        # determines how far pipe sticks out when pipe is on the ground
        if placement == 1:
            y = HEIGHT + randint(20,45)
            # places image on middle right bottom of screen
            self.rect = self.image.get_rect(midbottom = (x,y))
        # determines how far pipe sticks out when on top
        if placement == 2:
            # flips pipe vertically, but not horizontally
            self.image = pg.transform.flip(self.image, False, True)
            y = randint(-30, -10)
            # places image on middle right top of screen
            self.rect = self.image.get_rect(midtop = (x,y))
        self.pos = pg.math.Vector2(self.rect.topleft)
        # gets rid of transparent pixels in image so they cannot touch player
        self.mask = pg.mask.from_surface(self.image)
    # update method
    def update(self, delta_time):
        # speed of pipes
        self.pos.x -= 200 * delta_time
        self.rect.x = self.pos.x 
        # if pipe goes 200 units to the left of screen, delete it
        if self.rect.x <= -200:
            self.kill()

# runs game
Game().run()