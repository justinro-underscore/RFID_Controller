import time
import pygame
import random

pygame.init()

gameState = True
WIDTH = 500
LENGTH = 500
BALL_RAD = 20
PLAYER_L = 80
PLAYER_W = 20
PLAYER1_SPEED = 0
PLAYER2_SPEED = 0
PLAYER1_POS = WIDTH//2
PLAYER2_POS = WIDTH//2
BALL_POS = [WIDTH/2, LENGTH/2]
BALL_VEL = [4, 4]
SCOREBOARD_LENGTH = 50
SCORES = [0, 0]

gameDisplay = pygame.display.set_mode((WIDTH,LENGTH))

#title and Icon
pygame.display.set_caption('The best pong game ever')
logo = pygame.image.load('download.png')
pygame.display.set_icon(logo)

#colors
WHITE = (255,255,255)
BLACK = (0,0,0)

def keydown(event):
    global PLAYER1_SPEED, PLAYER2_SPEED 
    if event.key == pygame.K_UP:
        PLAYER2_SPEED = -8
    elif event.key == pygame.K_DOWN:
        PLAYER2_SPEED = 8
    elif event.key == pygame.K_w:
        PLAYER1_SPEED = -8
    elif event.key == pygame.K_s:
        PLAYER1_SPEED = 8

def keyup(event):
    global PLAYER1_SPEED, PLAYER2_SPEED

    if event.key in (pygame.K_w, pygame.K_s):
        PLAYER1_SPEED = 0
    elif event.key in (pygame.K_UP, pygame.K_DOWN):
        PLAYER2_SPEED = 0

def checkScore():
    for score in enumerate(SCORES):
        if score[1] >= 7:
            for i in range(100):
                print('player {} won!'.format(score[0]))
            exit()


def init_game():
    BALL_POS[0] = int((random.random() * (WIDTH - 40)) + 20)
    BALL_POS[1] = int(random.random() * (LENGTH - SCOREBOARD_LENGTH))

def draw_board(display):
    #making some variables global should be better but "eh its a hackathon" - Justin
    global BALL_POS, BALL_RAD, PLAYER1_POS, PLAYER_L, PLAYER_W, PLAYER1_SPEED, PLAYER2_POS, PLAYER2_SPEED
    
    gameDisplay.fill(BLACK)
    pygame.draw.line(gameDisplay, WHITE, [WIDTH / 2, 0],[WIDTH / 2, LENGTH], 1)
    pygame.draw.line(gameDisplay, WHITE, [PLAYER_W, 0],[PLAYER_W, LENGTH], 1)
    pygame.draw.line(gameDisplay, WHITE, [WIDTH - PLAYER_W, 0],[WIDTH - PLAYER_W, LENGTH], 1) 
    pygame.draw.line(gameDisplay, WHITE, [WIDTH / 2, 0],[WIDTH / 2, LENGTH], 1)
    pygame.draw.circle(gameDisplay, WHITE, [WIDTH//2, LENGTH//2], 70, 1)  
    
    #updating players position
    if (PLAYER1_POS > (PLAYER_L//2)) and (PLAYER1_POS < LENGTH - (PLAYER_W//2)):
        PLAYER1_POS += PLAYER1_SPEED
    elif PLAYER1_POS == PLAYER_L//2 and PLAYER1_SPEED < 0:
        PLAYER1_POS += PLAYER1_SPEED
    elif PLAYER1_POS == LENGTH - PLAYER_L//2 and PLAYER1_SPEED < 0:
        PLAYER1_POS += PLAYER1_SPEED

    if PLAYER2_POS > PLAYER_L//2 and PLAYER2_POS < LENGTH - PLAYER_W//2:
        PLAYER2_POS += PLAYER2_SPEED
    elif PLAYER2_POS == PLAYER_L//2 and PLAYER2_SPEED < 0:
        PLAYER2_POS += PLAYER2_SPEED
    elif PLAYER2_POS == LENGTH - PLAYER_L//2 and PLAYER2_SPEED < 0:
        PLAYER2_POS += PLAYER2_SPEED

    BALL_POS[0] += int(BALL_VEL[0])
    BALL_POS[1] += int(BALL_VEL[1])


    pygame.draw.circle(gameDisplay, WHITE, BALL_POS, BALL_RAD)
    pygame.draw.polygon(gameDisplay, WHITE, [[0, PLAYER1_POS - PLAYER_L//2], [PLAYER_W, PLAYER1_POS - PLAYER_L//2], [PLAYER_W, PLAYER1_POS + PLAYER_L//2],  [0, PLAYER1_POS + PLAYER_L//2]], 0)
    pygame.draw.polygon(gameDisplay, WHITE, [[WIDTH - PLAYER_W, PLAYER2_POS - PLAYER_L//2], [WIDTH, PLAYER2_POS - PLAYER_L//2], [WIDTH, PLAYER2_POS + PLAYER_L//2], [WIDTH - PLAYER_W, PLAYER2_POS + PLAYER_L//2]], 0)

    #ball collisions
    if int(BALL_POS[1]) <= BALL_RAD:
        BALL_VEL[1] = -BALL_VEL[1]
    if int(BALL_POS[1]) >= LENGTH - BALL_RAD:
        BALL_VEL[1] = -BALL_VEL[1]
    
    if int(BALL_POS[0]) <= BALL_RAD + PLAYER_W and int(BALL_POS[1]) in range(int(PLAYER1_POS) - PLAYER_L//2, int(PLAYER1_POS) + PLAYER_L//2, 1):
        BALL_VEL[0] = -BALL_VEL[0]
        BALL_VEL[0] *= 1.1
        BALL_VEL[1] *= 1.1
    elif int(BALL_POS[0]) <= BALL_RAD + PLAYER_W:
        SCORES[0] += 1
        checkScore()
        init_game()
    
    if int(BALL_POS[0]) >= WIDTH - BALL_RAD - PLAYER_W and int(BALL_POS[1]) in range(int(PLAYER2_POS) - PLAYER_L//2, int(PLAYER2_POS) + PLAYER_L//2, 1):
        BALL_VEL[0] = -BALL_VEL[0]
        BALL_VEL[0] *= 1.1
        BALL_VEL[1] *= 1.1
    elif int(BALL_POS[0]) >= WIDTH - BALL_RAD - PLAYER_W:
        SCORES[0] += 1
        checkScore()
        init_game()

    gameDisplay.blit(pygame.font.SysFont("Bernard MT", 30).render("Player 1: " + str(SCORES[0]), 1, WHITE), (50, 20))
    gameDisplay.blit(pygame.font.SysFont("Bernard MT", 30).render("Player 2: " + str(SCORES[1]), 1, WHITE), (340, 20))


#game event loop
init_game()
while gameState:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            keydown(event)
        elif event.type == pygame.KEYUP:
            keyup(event)
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    draw_board(gameDisplay)

    pygame.display.update()
