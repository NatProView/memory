import random

import pygame

import enum

from CardColor import CardColor
from Color import Color

pygame.init()
WIDTH = 600
HEIGHT = 600
GRID_WIDTH = 6
GRID_HEIGHT = 4
CARD_COUNT = GRID_HEIGHT * GRID_WIDTH
NUMBER_OF_PAIRS = CARD_COUNT // 2

fps = 60
timer = pygame.time.Clock()
new_grid = True
correct = []
options_list = []
spaces = []
used = []
colors_list = []
for i in enumerate(CardColor):
    card_dict = {
        "id": i[0] + 1,
        "name": i[1].name,
        "rgb": i[1].value
    }
    print(card_dict)
    colors_list.append(card_dict)

print(colors_list)


# create screen
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Memory Game")
title_font = pygame.font.Font('Roboto-Regular.ttf', 56)
small_font = pygame.font.Font('Roboto-Regular.ttf', 56)
pygame.init()


def draw_backgrounds():
    top_menu = pygame.draw.rect(screen, Color.black.value, [0, 0, WIDTH, 100])
    title_text = title_font.render('The Memory Game!', True, Color.white.value)
    screen.blit(title_text, (10, 20))
    board_space = pygame.draw.rect(screen, Color.gray.value, [0, 100, WIDTH, HEIGHT - 200], 0)
    bottom_menu = pygame.draw.rect(screen, Color.black.value, [0, HEIGHT - 100, WIDTH, 100], 0)


def draw_grid():
    global GRID_HEIGHT
    global GRID_WIDTH
    grid = []
    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            card = pygame.draw.rect(screen, Color.white.value, [i * 103 + 12, j * 100 + 112, 60, 80], 0, 4)
            grid.append(card)

    return grid

def generate_grid():
    global options_list
    global spaces
    for item in range(NUMBER_OF_PAIRS):
        options_list.append(item)

    for item in range(NUMBER_OF_PAIRS):
        card = options_list[random.randint(0, len(options_list) - 1)]
        spaces.append(card)

# main game loop
running = True
while running:
    timer.tick(fps)
    screen.fill(Color.white.value)
    if new_grid is True:
        generate_grid()
        new_grid = False
    draw_backgrounds()
    draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # wrzuc na ekran to co narysowales
    pygame.display.flip()
pygame.quit()

def log_error(msg):
    print(f"[ERROR] {msg}")


def log_debug(msg):
    print(f"[DEBUG] {msg}")


if CARD_COUNT % 2 != 0:
    err_string = "Nie można utworzyć gry - nieparzysta ilość pól"
    log_error(err_string)
    raise ValueError(err_string)


log_debug(f"Wymiary = {GRID_WIDTH}x{GRID_HEIGHT} => {NUMBER_OF_PAIRS} par")