#import pygame
#
#pygame.init()
#
#gameState = True
#WIDTH = 800
#LENGTH = 600
#gameDisplay = pygame.display.set_mode((WIDTH,LENGTH), 0, 32)
#
##title and Icon
#pygame.display.set_caption('The best pong game ever')
#logo = pygame.image.load('download.png')
#pygame.display.set_icon(logo)
#
##colors
#WHITE = (255,255,255)
#BLACK = (0,0,0)
#
##players
#pygame.draw.rect(gameDisplay, WHITE, (0, 0, 20, 10))
#pygame.draw.rect(gameDisplay, WHITE, (780, 590, 20, 10))
#
##game event loop
#while gameState:
#    for event in pygame.event.get():
#        if event.type == pygame.QUIT:
#            gameState = False
#
#    gameDisplay.fill((WHITE))
#    pygame.display.update()
import pygame

pygame.init()

h = input("Enter the height of the window : ")
w = input("Enter the width of the window : ")
screen = pygame.display.set_mode((int(w),int(h)))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=0
        #any additional event checks
    print('work?')
    screen.fill((0,0,255))
    #any additional drawings
    pygame.display.update()

pygame.quit()
