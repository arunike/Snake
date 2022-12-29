## Imports
import random
import sys
import time
import pygame
from pygame.locals import *
from collections import deque

## Screen size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 480
SIZE = 20
LINE_WIDTH = 1

## Scope dimensions
SCOPE_X = (0, SCREEN_WIDTH // SIZE - 1)
SCOPE_Y = (2, SCREEN_HEIGHT // SIZE - 1)

FOOD_STYLE_LIST = [(10, (255, 100, 100)), (20, (100, 255, 100)), (30, (100, 100, 255))] ## Food size, color

## Colors
LIGHT = (100, 100, 100)
DARK = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (200, 30, 30)
BGCOLOR = (40, 40, 60)

## Display messages
def print_text(screen, font, x, y, text, fcolor = (255, 255, 255)): 
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))

## Snake initialization
def init_snake():
    snake = deque() ## Snake body

    ## Initial snake length
    snake.append((2, SCOPE_Y[0]))
    snake.append((1, SCOPE_Y[0]))
    snake.append((0, SCOPE_Y[0]))

    return snake

## Food initialization
def create_food(snake):
    ## Randomly generate food coordinates
    food_x = random.randint(SCOPE_X[0], SCOPE_X[1])
    food_y = random.randint(SCOPE_Y[0], SCOPE_Y[1])

    while (food_x, food_y) in snake: ## Make sure the food is not on the snake
        food_x = random.randint(SCOPE_X[0], SCOPE_X[1])
        food_y = random.randint(SCOPE_Y[0], SCOPE_Y[1])

    return food_x, food_y

## Food style initialization
def get_food_style():
    return FOOD_STYLE_LIST[random.randint(0, 2)]

## Main program
def main():
    pygame.init() ## Initialize pygame
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) ## Create a window
    pygame.display.set_caption('Snake') ## Set the window title

    ## Create a font object
    font1 = pygame.font.SysFont('SimHei', 24) 
    font2 = pygame.font.Font(None, 72)
    fwidth, fheight = font2.size('GAME OVER')

    b = True ## Whether to change the direction

    snake = init_snake() ## Initialize the snake
    food = create_food(snake) ## Initialize the food
    food_style = get_food_style() ## Initialize the food style
    pos = (1, 0) ## Snake moving direction

    game_over = True ## Whether the game is over
    start = False ## Whether the game has started
    score = 0 ## Score
    orignalSpeed = 0.5 ## Original speed
    speed = orignalSpeed ## Current speed
    last_move_time = None ## Last move time
    pause = False ## Whether to pause

    while True: ## Main loop
        for event in pygame.event.get(): ## Event loop
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN: ## Keyboard event
                if event.key == K_RETURN: ## Press Enter to start the game
                    if game_over: ## If the game is over, start the game
                        start = True
                        game_over = False
                        b = True
                        snake = init_snake()
                        food = create_food(snake)
                        food_style = get_food_style()
                        pos = (1, 0)
                        score = 0
                        last_move_time = time.time()
                elif event.key == K_SPACE: ## Press space to pause
                    if not game_over: ## If the game is not over, pause
                        pause = not pause
                elif event.key in (K_w, K_UP): ## Press W or up arrow to change the direction
                    if b and not pos[1]: ## Make sure the snake is not moving vertically
                        pos = (0, -1)
                        b = False
                elif event.key in (K_s, K_DOWN): ## Press S or down arrow to change the direction
                    if b and not pos[1]: ## Make sure the snake is not moving vertically
                        pos = (0, 1)
                        b = False
                elif event.key in (K_a, K_LEFT): ## Press A or left arrow to change the direction
                    if b and not pos[0]: ## Make sure the snake is not moving horizontally
                        pos = (-1, 0)
                        b = False
                elif event.key in (K_d, K_RIGHT): ## Press D or right arrow to change the direction
                    if b and not pos[0]: ## Make sure the snake is not moving horizontally
                        pos = (1, 0)
                        b = False

        screen.fill(BGCOLOR) ## Fill the background color
        for x in range(SIZE, SCREEN_WIDTH, SIZE): ## Draw the grid
            pygame.draw.line(screen, BLACK, (x, SCOPE_Y[0] * SIZE), (x, SCREEN_HEIGHT), LINE_WIDTH)
        for y in range(SCOPE_Y[0] * SIZE, SCREEN_HEIGHT, SIZE): ## Draw the grid
            pygame.draw.line(screen, BLACK, (0, y), (SCREEN_WIDTH, y), LINE_WIDTH)

        if not game_over: ## If the game is not over
            curTime = time.time()
            if curTime - last_move_time > speed: ## If the time interval is greater than the speed
                if not pause: ## If not paused
                    b = True
                    last_move_time = curTime
                    next_s = (snake[0][0] + pos[0], snake[0][1] + pos[1])
                    if next_s == food: ## If the snake eats food
                        snake.appendleft(next_s)
                        score += food_style[0]
                        speed = orignalSpeed - 0.03 * (score // 100)
                        food = create_food(snake)
                        food_style = get_food_style()
                    else: ## If the snake does not eat food
                        if SCOPE_X[0] <= next_s[0] <= SCOPE_X[1] and SCOPE_Y[0] <= next_s[1] <= SCOPE_Y[1] \
                                and next_s not in snake: ## If the snake is within the scope and does not hit itself
                            snake.appendleft(next_s)
                            snake.pop()
                        else: ## If the snake is out of scope or hits itself
                            game_over = True

        if not game_over: ## If the game is not over
            pygame.draw.rect(screen, food_style[1], (food[0] * SIZE, food[1] * SIZE, SIZE, SIZE), 0)

        for s in snake: ## Draw the snake
            pygame.draw.rect(screen, DARK, (s[0] * SIZE + LINE_WIDTH, s[1] * SIZE + LINE_WIDTH,
                                            SIZE - LINE_WIDTH * 2, SIZE - LINE_WIDTH * 2), 0)

        print_text(screen, font1, 30, 7, f'Speed: {score // 100}')
        print_text(screen, font1, 150, 7, f'Press Enter to start')
        print_text(screen, font1, 450, 7, f'Score: {score}')

        if game_over: ## If the game is over
            if start: ## If the game has started
                print_text(screen, font2, (SCREEN_WIDTH - fwidth) // 2, (SCREEN_HEIGHT - fheight) // 2, 'GAME OVER', RED)

        pygame.display.update()

if __name__ == '__main__':
    main()