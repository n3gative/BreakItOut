#import pygame._view
import pygame
from pygame import *
import random
from random import randint,choice
import os
class Pad():
    def __init__(self):
        self.image = image.load(os.path.join('images','pad.png')).convert_alpha()
        self.rect  = self.image.get_rect()
        self.rect.bottomleft = (0,400)
        self.left = 0
        self.right = 0
    def moveBlit(self,surface,mousepos):
        x,y = self.rect.bottomright
        self.rect.topleft = ((mousepos[0],380))
        surface.blit(self.image,self.rect)

class Ball():
    def __init__(self,speed):
        self.time = 60
        self.x = random.choice((speed,-speed))
        self.y = -speed
        z = 0
        self.score = 0
        self.size = 2
        self.speed = 'normal'
        self.bounce = mixer.Sound(os.path.join('sounds','bounce.wav'))
        self.losehp = mixer.Sound(os.path.join('sounds','losehp.wav'))
        #hp paveiksleliai + kamuolio rectas
        self.image = image.load(os.path.join('images','ball.png')).convert_alpha()
        self.imagelives = image.load(os.path.join('images','hp.png')).convert_alpha()
        self.imagelivesbegin = image.load(os.path.join('images','hpb.png')).convert_alpha()
        self.imagelivesend = image.load(os.path.join('images','hpe.png')).convert_alpha()
        self.imagelivese = image.load(os.path.join('images','hpemp.png')).convert_alpha()
        self.imagelivesbe = image.load(os.path.join('images','hpbe.png')).convert_alpha()
        self.imagelivesee = image.load(os.path.join('images','hpee.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.lives = 8
        self.rect.bottomleft = (randint(10,400),randint(10,300))
    def checkCol(self,rectlist,surface,pad,mmb,font,blue):
        #tikrinam kolizija tarp visko :D
        if self.rect.left <= 0 :
            while self.rect.left <=0:
                self.rect.move_ip(1,0)
            self.x *= -1
        if self.rect.right >=450:
            while self.rect.right >=450:
                self.rect.move_ip(-1,0)
            self.x *=-1
        if self.rect.top <= 0 :
            self.y *= -1
        if self.rect.colliderect(pad) == True:
            self.y *= -1
        if self.rect.bottom >= 500:
            self.rect.bottom = 499
            self.lives -= 1
            self.losehp.play()
            self.y *= -1
        #tikrinam ar paspaude peles klavisa
        if mmb == True:
            if self.speed == 'normal':
                self.time = 60
            if self.speed == 'slow':
                if self.speed >20:
                    self.time -= 20
            if self.speed == 'fast':
                self.time += 20
            self.rect.move_ip(self.x,self.y)
        else:
            mx,my = mouse.get_pos()
            self.rect.topleft = (mx,365)
        surface.blit(self.image,self.rect)
        # piesiam hp bara ir score
        for i in xrange(1,9):
                if i == 1:
                    if self.lives >= i:
                        surface.blit(self.imagelivesbegin,(i*16+10,10))
                    else:
                        surface.blit(self.imagelivesbe,(i*16+10,10))
                elif i == 8:
                    if self.lives >= i:
                        surface.blit(self.imagelivesend,(i*16+10,10))
                    else:
                        surface.blit(self.imagelivesee,(i*16+10,10))
                else:
                    if self.lives >= i:
                        surface.blit(self.imagelives,(i*16+10,10))
                    else:
                        surface.blit(self.imagelivese,(i*16+10,10))
                scoreBoard = font.render(str(self.score),True,blue)
                surface.blit(scoreBoard,(200,10))

class Brick():
    def __init__(self,pos,blockType):
        self.type = blockType
        self.hp = self.type
        self.image = image.load(os.path.join('images','brick.png')).convert()
        self.image2 = image.load(os.path.join('images','brick2.png')).convert()
        self.image3 = image.load(os.path.join('images','brick3.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.pickupList = []
    def blitas(self,surface,ball):
        if self.hp > 0:
            #bricko ir kamuolio kolizija
            if self.rect.colliderect(ball.rect) == True:
                ball.x *= -1
                ball.y *= -1
                self.hp -= 1
                ball.score += 10
                ball.bounce.play
                if randint(1,10) == 5:
                    self.pickupList.append(Pickup(self.rect))
                if ball.score %500 == 0:
                    if ball.x >0:
                        ball.x += 1
                    else:
                        ball.x -=1
                    if ball.y < 0:
                        ball.y -= 1
                    else:
                        ball.y += 1
            if self.hp ==1:
                surface.blit(self.image,self.rect)
            elif self.hp == 2:
                surface.blit(self.image2,self.rect)
            else:
                surface.blit(self.image3,self.rect)
class Pickup:
    def __init__(self,brickrect):
        self.type = randint(1,5)
        self.image = image.load(os.path.join('images','pickup'+str(self.type)+'.PNG'))
        self.rect = self.image.get_rect()
        self.alive = True
        self.rect.topleft = brickrect.center
    def Move(self,pad,surface,ball):
        if self.rect.colliderect(pad.rect) == False:
            if self.alive == True:
                surface.blit(self.image,self.rect)
        else:
            self.alive = False
            if self.type ==1:
                temp = ball.rect.topleft
                if ball.size == 2:
                    ball.image = image.load(os.path.join('images','ball_small.png'))
                    ball.size = 1
                if ball.size == 3:
                    ball.image = image.load(os.path.join('images','ball.png'))
                    ball.size = 2
                ball.rect = ball.image.get_rect()
                ball.rect.topleft = temp
            if self.type == 2:
                temp = ball.rect.topleft
                if ball.size == 2:
                    ball.image = image.load(os.path.join('images','ball_big.png'))
                if ball.size == 1:
                    ball.image = image.load(os.path.join('images','ball.png'))
                ball.rect = ball.image.get_rect()
                ball.rect.topleft = temp
            if self.type == 3:
                temp = pad.rect.topleft
                pad.image = image.load(os.path.join('images','pad_big.png')).convert_alpha()
                pad.rect = pad.image.get_rect()
                pad.rect.topleft = temp
            if self.type == 4:
                temp = pad.rect.topleft
                pad.image = image.load(os.path.join('images','pad_small.png')).convert_alpha()
                pad.rect = pad.image.get_rect()
                pad.rect.topleft = temp
            if self.type == 5:
                ball.lives = 8
        self.rect.move_ip(0,1)
        x,y = self.rect.topleft
        if y >= 531:
            self.alive = False

#optiom funkcija
def Options(surface):
    optionsImage = image.load(os.path.join('images','optionsmenu.png'))
    global diff
    global speed
    still = 1
    while still:
        surface.blit(optionsImage,(0,0))
        display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                still = 0

#main arba meniu funkcija
def main():
    levelBlockList= [
    #1 lygis
    [(0,100),(32,100),(64,100),(96,100),(128,100),(160,100),(192,100),(224,100),(256,100),(288,100),(320,100),(352,100),(384,100),(416,100),
    (0,116),(32,116),(64,116),(96,116),(128,116),(160,116),(192,116),(224,116),(256,116),(288,116),(320,116),(352,116),(384,116),(416,116),
    (0,132),(32,132),(64,132),(96,132),(128,132),(160,132),(192,132),(224,132),(256,132),(288,132),(320,132),(352,132),(384,132),(416,132)
    ,(0,148),(32,148),(64,148),(96,148),(128,148),(160,148),(192,148),(224,148),(256,148),(288,148),(320,148),(352,148),(384,148),(416,148),
    (0,164),(32,164),(64,164),(96,164),(128,164),(160,164),(192,164),(224,164),(256,164),(288,164),(320,164),(352,164),(384,164),(416,164)],

    #2 lygis
    [(64,100),(96,100),(128,100),(160,100),(192,100),(224,100),(256,100),(288,100),(320,100),(352,100),
     (32,116),(64,116),(96,116),(128,116),(160,116),(192,116),(224,116),(256,116),(288,116),(320,116),(352,116),(384,116),
     (0,132),(64,132),(96,132),(128,132),(160,132),(192,132),(224,132),(256,132),(288,132),(320,132),(352,132),(416,132),
     (0,148),(64,148),(96,148),(128,148),(160,148),(192,148),(224,148),(256,148),(288,148),(320,148),(352,148),(416,148),
     (0,164),(64,164),(96,164),(128,164),(160,164),(192,164),(224,164),(256,164),(288,164),(320,164),(352,164),(416,164),
     (0,180),(64,180),(96,180),(128,180),(160,180),(192,180),(224,180),(256,180),(288,180),(320,180),(352,180),(416,180),
     (0,196),(96,196),(128,196),(160,196),(192,196),(224,196),(256,196),(288,196),(320,196),(416,196),
     (128,212),(160,212),(192,212),(224,212),(256,212),(288,212),
     (160,228),(192,228),(224,228),(256,228),
     (128,244),(160,244),(192,244),(224,244),(256,244),(288,244),
     (64,148),(96,260),(128,260),(160,260),(192,260),(224,260),(256,260),(288,260),(320,260)

    ]
    #3lygis
    ]
    levelBlockTypes= [
    #1 lygis
    [1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3],
    #2 lygis
    [2,2,2,2,2,2,2,2,2,2,2,2,1,3,1,1,1,1,3,1,2,2,2,2,1,3,1,1,1,1,3,1,2,2,2,2,1,3,1,1,1,1,3,1,2,2,2,2,1,1,1,1,1,1,1,1,2,2,2,2,1,1,1,
    1,1,1,1,1,2,2,2,2,1,3,3,3,3,1,2,2,2,1,1,1,1,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
    ]
    diff = 'easy'
    speed = 4
    pygame.init()
    running = 1
    gameIsOver = False
    menuscreen = display.set_mode((450,500))
    display.set_caption('Breakout 0.4 Beta')
    menuimage = image.load(os.path.join('images','menu.png')).convert()
    start = image.load(os.path.join('images','start.png')).convert_alpha()
    options = image.load(os.path.join('images','options.png')).convert_alpha()
    optionsRect = options.get_rect()
    startRect = start.get_rect()
    startRect.topleft = (50,200)
    optionsRect.topleft = (50,250)
    mouseRect = Rect((1,1),(1,1))
    mouseRect.topleft = mouse.get_pos()
    menuRunning = 1
    song =  pygame.mixer.music.load(os.path.join('sounds','music','Billions And Billions.mp3'))
    mixer.music.play(1)

    while menuRunning:
        for event in pygame.event.get():
            mouseRect.topleft = mouse.get_pos()
            if event.type == pygame.QUIT:
                menuRunning = 0
            if event.type == MOUSEBUTTONDOWN:
                gameIsOver = False
                if mouseRect.colliderect(startRect) == True:
                    for i in xrange(0,2):
                        if gameIsOver == False:
                            Game(levelBlockList[i],levelBlockTypes[i],speed)
                if mouseRect.colliderect(optionsRect) == True:
                    Options(menuscreen)

        menuscreen.blit(menuimage,(0,0))
        menuscreen.blit(start,startRect)
        menuscreen.blit(options,optionsRect)
        display.flip()
#grid dydis = 14x16
def Game(blockList,blockTypes,speed):
    global gameIsOver
    screenRes = (450,500)
    screen = display.set_mode(screenRes)
    display.set_caption('BreakItOut 0.2')
    gameRunning = 1
    blue = (131,244,168)
    fullScreen =0
    mousepos = [0,0]
    bg = image.load(os.path.join('images','bg.png'))
    fontas = font.Font('04b08.ttf',14)
    fontas28 = font.Font('04b08.ttf',28)
    def gameOver(fontas,clock,blue):
        gameOver = fontas.render('Game over',True,blue)
        clock.tick(5)
        screen.fill((0,0,0))
        screen.blit(gameOver,(150,180))
    ball = Ball(speed)
    padas = Pad()
    start = fontas.render('Press mouse button to begin',True,blue)
    brickList = []
    cheatMode = False
    mmb = False
    lives = fontas.render('HP',True,blue)
    brickPosList = blockList
    #pridedam Block objektu su iskart nustatytom koordinatem ir tipu
    for i in xrange(0,len(brickPosList)):
        brickList.append(Brick(brickPosList[i],blockTypes[i]))
    clock = pygame.time.Clock()
    while gameRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameIsOver = False
                gameRunning = 0

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    gameIsOver = True
                    gameRunning = 0
                if event.key == K_l:
                    cheatMode = True
                if event.key == K_g:
                    gameOver(fontas28,clock,blue)

            if event.type == MOUSEBUTTONDOWN:
                mmb = True
        if ball.lives >= 1:
            mousepos = mouse.get_pos()
            screen.fill((212,0,12))
            screen.blit(bg,(0,0))
            screen.blit(lives,(26,28))
            if mmb == False:
                screen.blit(start,(20,300))
            ball.checkCol(brickList,screen,padas,mmb,fontas,blue)
            padas.moveBlit(screen,mousepos)
            for i in xrange(0,len(brickList)):
                if brickList[i].type !=0:
                    brickList[i].blitas(screen,ball)
                    for i2 in xrange(0,len(brickList[i].pickupList)):
                        brickList[i].pickupList[i2].Move(padas,screen,ball)
            clock.tick(ball.time)
            if cheatMode == False:
                brickAmount = 0
                for i in xrange(0,len(brickList)):
                    if brickList[i].hp >0:
                        brickAmount += 1
                blokai = fontas.render('Blocks left:'+str(brickAmount),True,blue)
            if cheatMode == True:
                brickAmount = 0
            if brickAmount == 0:
                gameIsOver = False
                gameRunning = 0
            screen.blit(blokai,(200,20))
        else:
            gameIsOver = True
            gameOver(fontas28,clock,blue)
        display.flip()





if __name__ == '__main__':
    main()
