import time
import pygame
import random

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.init()

gameState = True
WIDTH = 1000
LENGTH = 800
BALL_RAD = 20
PLAYER_L = 120
PLAYER_W = 20
PLAYER_OFFSET = 30
PLAYER_SPEED = 4
PLAYER1_SPEED = 0
PLAYER2_SPEED = 0

PLAYER1_POS = WIDTH//2
PLAYER2_POS = WIDTH//2
BALL_POS = [WIDTH/2, LENGTH/2]
STARTING_BALL_VEL = [2, 1]
BALL_VEL = list(STARTING_BALL_VEL)
BALL_HIT_VAL = 1.3
LAST_WINNER = 0
SCOREBOARD_LENGTH = 50
SCORES = [0, 0]

gameDisplay = pygame.display.set_mode((WIDTH,LENGTH))

#title and Icon
pygame.display.set_caption('The best pong game ever')
logo = pygame.image.load('download.png')
pygame.display.set_icon(logo)
BOOP = pygame.mixer.Sound('Boop.wav')
HIGH_BOOP = pygame.mixer.Sound('HighBoop.wav')

#colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)

def keydown(event):
    global PLAYER1_SPEED, PLAYER2_SPEED 
    if event.key == pygame.K_UP:
        PLAYER2_SPEED = -PLAYER_SPEED
    elif event.key == pygame.K_DOWN:
        PLAYER2_SPEED = PLAYER_SPEED
    elif event.key == pygame.K_w:
        PLAYER1_SPEED = -PLAYER_SPEED
    elif event.key == pygame.K_s:
        PLAYER1_SPEED = PLAYER_SPEED

def keyup(event):
    global PLAYER1_SPEED, PLAYER2_SPEED

    if event.key in (pygame.K_w, pygame.K_s):
        PLAYER1_SPEED = 0
    elif event.key in (pygame.K_UP, pygame.K_DOWN):
        PLAYER2_SPEED = 0

def checkScore():
    for score in enumerate(SCORES):
        if score[1] >= 7:
            return True
    return False


def init_game():
    BALL_POS[0] = (WIDTH // 2) + int((1 * 160) - 80)
    BALL_POS[1] = int(1 * (LENGTH - 4 * (BALL_RAD)) + (2 * BALL_RAD))
    BALL_VEL[0] = (-1 if LAST_WINNER == 0 else 1) * STARTING_BALL_VEL[0]
    BALL_VEL[1] = (1 if (PLAYER1_POS if LAST_WINNER == 0 else PLAYER2_POS) > (LENGTH // 2) else -1) * STARTING_BALL_VEL[1]

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
    if (PLAYER1_POS >= (LENGTH - (PLAYER_L // 2))):
        PLAYER1_POS = LENGTH - (PLAYER_L // 2) - 1
    elif (PLAYER1_POS <= (PLAYER_L // 2)):
        PLAYER1_POS = (PLAYER_L // 2) + 1

    if PLAYER2_POS > PLAYER_L//2 and PLAYER2_POS < LENGTH - PLAYER_W//2:
        PLAYER2_POS += PLAYER2_SPEED
    elif PLAYER2_POS == PLAYER_L//2 and PLAYER2_SPEED < 0:
        PLAYER2_POS += PLAYER2_SPEED
    elif PLAYER2_POS == LENGTH - PLAYER_L//2 and PLAYER2_SPEED < 0:
        PLAYER2_POS += PLAYER2_SPEED
    if (PLAYER2_POS >= (LENGTH - (PLAYER_L // 2))):
        PLAYER2_POS = LENGTH - (PLAYER_L // 2) - 1
    elif (PLAYER2_POS <= (PLAYER_L // 2)):
        PLAYER2_POS = (PLAYER_L // 2) + 1

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
    
    finished = False
    if int(BALL_POS[0]) <= BALL_RAD + PLAYER_W and int(BALL_POS[1]) in range(int(PLAYER1_POS) - PLAYER_L//2 - PLAYER_OFFSET, int(PLAYER1_POS) + PLAYER_L//2 + PLAYER_OFFSET, 1):
        BOOP.play()
        BALL_VEL[0] = -BALL_VEL[0]
        BALL_VEL[0] *= BALL_HIT_VAL
        BALL_VEL[1] *= BALL_HIT_VAL
    elif int(BALL_POS[0]) <= BALL_RAD + PLAYER_W:
        HIGH_BOOP.play()
        SCORES[0] += 1
        LAST_WINNER = 0
        finished = finished or checkScore()
        init_game()
    
    if int(BALL_POS[0]) >= WIDTH - BALL_RAD - PLAYER_W and int(BALL_POS[1]) in range(int(PLAYER2_POS) - PLAYER_L//2 - PLAYER_OFFSET, int(PLAYER2_POS) + PLAYER_L//2 + PLAYER_OFFSET, 1):
        BOOP.play()
        BALL_VEL[0] = -BALL_VEL[0]
        BALL_VEL[0] *= BALL_HIT_VAL
        BALL_VEL[1] *= BALL_HIT_VAL
    elif int(BALL_POS[0]) >= WIDTH - BALL_RAD - PLAYER_W:
        HIGH_BOOP.play()
        SCORES[1] += 1
        LAST_WINNER = 1
        finished = finished or checkScore()
        init_game()

    gameDisplay.blit(pygame.font.SysFont("Monospace", 40).render("Player 1: " + str(SCORES[0]), 1, WHITE), (120, 20))
    gameDisplay.blit(pygame.font.SysFont("Monospace", 40).render("Player 2: " + str(SCORES[1]), 1, WHITE), (620, 20))

    if finished:
        winner = "Player {} wins!".format(1 if SCORES[0] > SCORES[1] else 2)
        starting_pos_x = 100
        pos_y = 430
        offset = 10
        size_of_char = 60
        pygame.draw.polygon(gameDisplay, WHITE, [[starting_pos_x - offset, pos_y - offset],
                                                 [starting_pos_x - offset, pos_y + size_of_char + 45 + offset],
                                                 [starting_pos_x + (size_of_char * len(winner)) + offset, pos_y + size_of_char + 45 + offset],
                                                 [starting_pos_x + (size_of_char * len(winner)) + offset, pos_y - offset]], 0)
        whitespace_num = 0
        for i, c in enumerate(winner):
            if c == " ":
                whitespace_num += 1
            gameDisplay.blit(pygame.font.SysFont("Monospace", 120).render(c, 1, RED if (i + whitespace_num) % 2 == 0 else BLUE), (starting_pos_x + (i * size_of_char), pos_y - 20))
    return finished


#game event loop
init_game()

finished = False
while gameState:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            keydown(event)
        elif event.type == pygame.KEYUP:
            keyup(event)
        elif event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if not finished:
        finished = draw_board(gameDisplay)

        pygame.display.update()
