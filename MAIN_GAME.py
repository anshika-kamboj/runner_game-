import pygame
from pygame.locals import *
import os
import sys 
import math
import random

pygame.init()

W,H=800,447
win = pygame.display.set_mode((W,H))
pygame.display.set_caption('RUNNER..')

bg=pygame.image.load(os.path.join('images','bg.png')).convert()
bgX = 0
bgX2 = bg.get_width()

clock = pygame.time.Clock()

class player(object):
    run =  [pygame.image.load(os.path.join('images',str(x)+'.png'))for x in range(8,16)]
    jump = [pygame.image.load(os.path.join('images',str(x)+'.png'))for x in range(1,8)]
    s1=pygame.image.load(os.path.join('images', 'S1.png'))
    s2=pygame.image.load(os.path.join('images', 'S2.png'))
    s3= pygame.image.load(os.path.join('images', 'S3.png'))
    s4=pygame.image.load(os.path.join('images', 'S4.png'))
    s5=pygame.image.load(os.path.join('images', 'S5.png'))
    slide = [s1,s2,s2,s2, s2,s2,s2,s2,s3, s4, s5]
    fall = pygame.image.load(os.path.join('images','0.png'))
    jumpList = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.sliding = False
        self.falling = False # NEW
        self.slideCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.slideUp = False

    def draw(self, win):
        if self.falling: # NEW
            win.blit(self.fall, (self.x, self.y + 30))
            
        elif self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 1.3
            win.blit(self.jump[self.jumpCount//18], (self.x,self.y))
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0
            self.hitbox = (self.x+ 4,self.y,self.width-24,self.height-10) 
        elif self.sliding or self.slideUp:
            if self.slideCount < 20:
                self.y += 1
                self.hitbox = (self.x+ 4,self.y,self.width-24,self.height-10) # NEW
            elif self.slideCount == 80:
                self.y -= 19
                self.sliding = False
                self.slideUp = True
            elif self.slideCount > 20 and self.slideCount < 80: # NEW
                self.hitbox = (self.x,self.y+3,self.width-8,self.height-35) # NEW
                
            if self.slideCount >= 110:
                self.slideCount = 0
                self.runCount = 0
                self.slideUp = False
                self.hitbox = (self.x+ 4,self.y,self.width-24,self.height-10) # NEW
            win.blit(self.slide[self.slideCount//10], (self.x,self.y))
            self.slideCount += 1
            
        else:
            if self.runCount > 42:
                self.runCount = 0
            win.blit(self.run[self.runCount//6], (self.x,self.y))
            self.runCount += 1
            self.hitbox = (self.x+ 4,self.y,self.width-24,self.height-13) # NEW
 
        #pygame.draw.rect(win, (255,0,0),self.hitbox, 2) # NEW - Draws hitbox


class saw(object):
    rotate = [pygame.image.load(os.path.join('images', 'SAW0.PNG')),pygame.image.load(os.path.join('images', 'SAW1.PNG')),pygame.image.load(os.path.join('images', 'SAW2.PNG')),pygame.image.load(os.path.join('images', 'SAW3.PNG'))]
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotateCount = 0
        self.vel = 1.4
        
    def collide(self,rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False    

    def draw(self,win):
        self.hitbox = (self.x + 10, self.y + 5, self.width - 20, self.height - 5)  # Defines the accurate hitbox for our character 
        #pygame.draw.rect(win, (120,0,0), self.hitbox, 1)
        if self.rotateCount >= 8:  # This is what will allow us to animate the saw
            self.rotateCount = 0
        win.blit(pygame.transform.scale(self.rotate[self.rotateCount//2], (64,64)), (self.x,self.y))  # scales our image down to 64x64 before drawing
        self.rotateCount += 1
        
        
class spike(saw):  # We are inheriting from saw
    img = pygame.image.load(os.path.join('images', 'spike.png'))
    def draw(self,win):
        self.hitbox = (self.x + 10, self.y, 28,315)  # defines the hitbox
        #pygame.draw.rect(win, (100,0,0), self.hitbox, 1)
        win.blit(self.img, (self.x,self.y))
        
    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] < self.hitbox[3]:
                return True
        return False    
 
def updateFile():
    f = open('scores.txt','r') # opens the file in read mode
    file = f.readlines() # reads all the lines in as a list
    last = int(file[0]) # gets the first line of the file

    if last < int(score): # sees if the current score is greater than the previous best
        f.close() # closes/saves the file
        file = open('scores.txt', 'w') # reopens it in write mode
        file.write(str(score)) # writes the best score
        file.close() # closes/saves the file

        return score
               
    return last
            
def endScreen():
    global pause, score, speed, obstacles
    # We need to reset our variables
    pause = 0
    speed = 30
    obstacles = []
                 
    # another game loop  
    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN: # if the user hits the mouse button
                run = False
                runner.falling = False
                runner.sliding = False
                runner.jumpin = False
        
        # This will draw text displaying the score to the screen.      
        win.blit(bg, (0,0))
        largeFont = pygame.font.SysFont('comicsans', 80) # creates a font object
        lastScore = largeFont.render('Best Score: ' + str(updateFile()),1,(30,20,20)) # We will create the function updateFile later
        currentScore = largeFont.render('Score: '+ str(score),1,(50,40,40))
        win.blit(lastScore, (W/2 - lastScore.get_width()/2,100))
        win.blit(currentScore, (W/2 - currentScore.get_width()/2, 25))
        pygame.display.update()
    score = 0 
    
                        
#redraw background function
def redrawWindow():
    largeFont = pygame.font.SysFont('comicsans', 30) # Font object
    win.blit(bg, (bgX, 0))
    win.blit(bg, (bgX2,0))
    text = largeFont.render('Score: ' + str(score), 1, (50,40,40)) # create our text
    runner.draw(win)
    for obstacle in obstacles:
        obstacle.draw(win)

    win.blit(text, (600, 10)) # draw the text to the screen
    pygame.display.update()
        
 

    

pygame.time.set_timer(USEREVENT+1, 800) #set timer for 0.8 seconds
pygame.time.set_timer(USEREVENT+2, random.randrange(3000, 4000)) # Will trigger every 2 - 3.5 seconds
#main running loop
speed = 30
score=0

run = True
runner = player(200,313,64,64)

fallSpeed = 0
pause = 0

obstacles = []

while run:
    if pause > 0:
        pause += 1
        if pause > fallSpeed * 2:
            endScreen()
        
    score = speed//10 - 3

    for obstacle in obstacles:
        if obstacle.collide(runner.hitbox):
            runner.falling = True
            
            if pause == 0:
                pause = 1
                fallSpeed = speed
        if obstacle.x < -64:
            obstacles.pop(obstacles.index(obstacle))
        else:
            obstacle.x -= 1.4
    
    bgX -= 1.4
    bgX2 -= 1.4

    if bgX < bg.get_width() * -1:
        bgX = bg.get_width()
    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width() 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            
        if event.type == USEREVENT+1:
            speed += 1
            
        if event.type == USEREVENT+2:
            r = random.randrange(0,2)
            if r == 0:
                obstacles.append(saw(810, 310, 64, 64))
            elif r == 1:
                obstacles.append(spike(810, 0, 48, 310))
                
    if runner.falling == False:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            if not(runner.jumping):
                runner.jumping = True

        if keys[pygame.K_DOWN]:
            if not(runner.sliding):
                runner.sliding = True

    clock.tick(speed)
    redrawWindow()
           
            
    
                
        