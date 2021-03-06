# Please Jeff Goldblum or suffer
import time
import random
import pygame
from pygame.locals import *

# Ball boy
class Pong(object):
    def __init__(self, screensize):

        self.screensize = screensize

        # center of screen
        self.centerx = int(screensize[0]*0.5)
        self.centery = int(screensize[1]*0.5)

        self.radius = 8

        # set size
        self.rect = pygame.Rect(self.centerx-self.radius,
                                self.centery-self.radius,
                                self.radius*2, self.radius*2)

        self.color = (255, 255, 255)

        # starting point of ball
        diry = random.randint(-5,-1)
        dirx = random.randint(1, 5)
        self.direction = [diry ,dirx] # sets direction random

        self.speedx = 3
        self.speedy = 5

        self.hit_edge_left = False
        self.hit_edge_right = False

    def update(self, player_paddle, ai_paddle):

        # new spot of paddle
        self.centerx += self.direction[0]*self.speedx
        self.centery += self.direction[1]*self.speedy
        self.rect.center = (self.centerx, self.centery)

        # set walls
        if self.rect.top <= 0:  # hits top, goes down
            self.direction[1] = 1
        elif self.rect.bottom >= self.screensize[1]-1:
            self.direction[1] = -1

        if self.rect.right >= self.screensize[0]-1: # condition to win
            self.hit_edge_right = True
        elif self.rect.left <= 0:   # condition if lose
            self.hit_edge_left = True

        # This is for when pong hits paddles
        if self.rect.colliderect(player_paddle.rect):
            self.direction[0] = -1
        if self.rect.colliderect(ai_paddle.rect):
            self.direction[0] = 1

        if time.clock() > 1:  # introduces acceleration
            self.speedx += float(0.01)


    def render(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius, 0)

# Opponent
class AIPaddle(object):
    def __init__(self, screensize):

        self.centerx = 5
        self.centery = int(screensize[1]*0.5)

        self.height = 100
        self.width = 10

        self.rect = pygame.Rect(0, self.centery-int(self.height*0.5), self.width, self.height)

        self.color = (0, 0, 0)

        self.speed = 10

    def update(self, pong):
        if pong.rect.top < self.rect.top:
            self.centery -= self.speed
        elif pong.rect.bottom > self.rect.bottom:
            self.centery += self.speed

        self.rect.center = (self.centerx, self.centery)

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, (0,0,0), self.rect, 1)

# Player
class PlayerPaddle(object):
    def __init__(self, screensize):
        self.screensize = screensize
        self.centerx = screensize[0]-5
        self.centery = int(screensize[1]*0.5)

        self.height = 100
        self.width = 10

        self.rect = pygame.Rect(0, self.centery-int(self.height*0.5), self.width, self.height)

        self.color = (0, 0, 0)

        self.speed = 7  # how fast player reacts to pong
        self.direction = 0

    def update(self):
        self.centery += self.direction*self.speed

        self.rect.center = (self.centerx, self.centery)
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screensize[1]-1:
            self.rect.bottom = self.screensize[1]-1

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, (0,0,0), self.rect, 1)

# startscreen class
class Go(object):
    def __init__(self, screen, screensize, wins, losses):
        self.screensize = screensize
        self.screen = screen
        self.wins = wins
        self.losses = losses

        self.start = StartScreen('GOLDY.png', [(self.screensize[0]/1.75),50]) # Places Goldblum's head just right

        self.prompt = pygame.font.SysFont('Comic Sans', 48)
        self.text = self.prompt.render('PRESS SPACE TO ENTER MY DOJO', True, (0,0,0))
        self.win_count = self.prompt.render('TIMES YOU CHEATED: %s' %self.wins, True, (0,0,0))
        self.losses_count = self.prompt.render("TIMES YOU'VE BEEN CRUSHED: %s" %self.losses, True, (0,0,0))

        self.screen.fill([255, 255, 255])

        self.screen.blit(self.start.image, self.start.rect)
        self.screen.blit(self.text, (0,15))
        self.screen.blit(self.win_count, (0, 390))
        self.screen.blit(self.losses_count, (0, 420))

        pygame.display.set_caption("WELCOME TO BLUM'S HOUSE, BABY")
        pygame.display.flip()


# startscreen referenced in Go
class StartScreen(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

# Goldblum's big beautiful face of a background
class Goldblum(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def main():
    sit = True
    running = False

    wins = 0
    losses = 0

    pygame.init()
    pygame.font.init()
    screensize = (945,480)
    screen = pygame.display.set_mode(screensize)
    clock = pygame.time.Clock()

    # game loop
    while sit:

        # start screen go
        go = Go(screen, screensize, wins, losses)
        for event in pygame.event.get():
            if event.type == QUIT:
                sit = False
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    running = True
                if event.key == K_ESCAPE:
                    sit = False

        pong = Pong(screensize)
        ai_paddle = AIPaddle(screensize)
        player_paddle = PlayerPaddle(screensize)
        BackGround = Goldblum('Goldenflame.png', [0,0])

        # gameplay loop
        while running:
            # fps limiter
            clock.tick(100)

            # event handling phase
            for event in pygame.event.get():

                if event.type == QUIT:
                    running = False
                    sit = False

                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        player_paddle.direction = -1
                    if event.key == K_DOWN:
                        player_paddle.direction =  1
                    if event.key == K_ESCAPE:
                        running = False
                if event.type == KEYUP:
                    if event.key == K_UP and player_paddle.direction == -1:
                        player_paddle.direction = 0
                    if event.key == K_DOWN and player_paddle.direction == 1:
                        player_paddle.direction = 0

            # object updating phase
            ai_paddle.update(pong)
            player_paddle.update()
            pong.update(player_paddle, ai_paddle)

            if pong.hit_edge_left:
                wins +=1
                running = False
            elif pong.hit_edge_right:
                losses +=1
                running = False

            # rendering phase
            screen.fill([255, 255, 255])
            screen.blit(BackGround.image, BackGround.rect)
            pygame.display.set_caption('I SUFFER NO RIVAL')

            ai_paddle.render(screen)
            player_paddle.render(screen)
            pong.render(screen)
            pygame.display.flip()

main()
 
