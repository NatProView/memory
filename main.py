import os
import random
import time

import pygame

import enum

from CardColor import CardColor
from Color import Color

# debug mode
debug = False

# start Pygame and define variables
pygame.init()
pygame.mixer.init()
timer = pygame.time.Clock()

# pygame mixer
s_dir = 'sound'
pygame.mixer.music.load(os.path.join(s_dir, 'bkg.mp3'))
match_sound_effect = pygame.mixer.Sound(os.path.join(s_dir, 'match.mp3'))
pygame.mixer.music.play(-1)

# states
EMPTY = 0
MATCHED = 1
CHECKED = 2

# game config
fps = 60
WIDTH = 600
HEIGHT = 600
GRID_WIDTH = 6
GRID_HEIGHT = 4
CARD_COUNT = GRID_HEIGHT * GRID_WIDTH
NUMBER_OF_PAIRS = CARD_COUNT // 2

# load list of colors available to use for non-card entities
color_list = []
for c in enumerate(CardColor):
    color_list.append((c[0], c[1].value))
print(color_list)

# game state variables
new_grid = True
first_guess = False
second_guess = False
restart_var = False
is_game_over = False

first_guess_num = 0
second_guess_num = 0
matched_pairs = 0
turns = 0

# matrix of correct guesses
correct = [[0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0]]

options_list = []
spaces = []
used = []

# create screen
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
pygame.display.set_caption("Memory Game")
title_font = pygame.font.Font('Roboto-Regular.ttf', 56)
small_font = pygame.font.Font('Roboto-Regular.ttf', 40)


def log_error(msg):
    print(f"[ERROR] {msg}")


def log_debug(msg):
    if debug:
        print(f"[DEBUG] {msg}")


def draw_backgrounds():
    global turns
    global matched_pairs
    top_menu = pygame.draw.rect(screen, Color.primary.value, [0, 0, WIDTH, 100])
    title_text = title_font.render('The Memory Game!', True, Color.white.value)
    screen.blit(title_text, (55, 20))
    board_space = pygame.draw.rect(screen, Color.light_primary.value, [0, 100, WIDTH, HEIGHT - 200], 0)
    bottom_menu = pygame.draw.rect(screen, Color.primary.value, [0, HEIGHT - 100, WIDTH, 100], 0)
    restart_button = pygame.draw.rect(screen, Color.accent.value, [415, HEIGHT - 85, 145, 60], 0)
    restart_button_frame = pygame.draw.rect(screen, Color.primary_text.value, [415, HEIGHT - 85, 145, 60], 3, 4)
    turn_text = small_font.render(f"Turns: {turns}", True, Color.white.value)
    matches_text = small_font.render(f"Matches: {matched_pairs}", True, Color.white.value)
    restart_text = small_font.render('Restart', True, Color.white.value)
    screen.blit(turn_text, (20, HEIGHT - 80))
    screen.blit(matches_text, (200, HEIGHT - 80))
    screen.blit(restart_text, (420, HEIGHT - 80))

    return restart_button


def draw_grid():
    global GRID_HEIGHT
    global GRID_WIDTH
    global spaces
    global correct
    global color_list
    grid = []
    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            if correct[j][i] == EMPTY:
                card = pygame.draw.rect(screen, Color.white.value, [i * 103 + 12, j * 100 + 112, 60, 80], 0, 4)
            else:
                this_it_color = color_list[spaces[i * GRID_HEIGHT + j]][1]
                card = pygame.draw.rect(screen, this_it_color, [i * 103 + 12, j * 100 + 112, 60, 80], 0, 4)
            # print(f"[TIS COLOR] {this_it_color}")
            grid.append(card)
            if debug:
                card_text = small_font.render(f'{spaces[i * GRID_HEIGHT + j]}', True, Color.gray.value)
                screen.blit(card_text, (i * 103 + 18, j * 100 + 120))

    for x in range(GRID_HEIGHT):
        for y in range(GRID_WIDTH):
            if correct[x][y] == MATCHED:
                card = pygame.draw.rect(screen, Color.green.value, [y * 103 + 12, x * 100 + 112, 60, 80], 3, 4)
                if debug:
                    card_text = small_font.render('X', True, Color.gray.value)
                    screen.blit(card_text, (y * 103 + 18, x * 100 + 120))

    return grid


def generate_grid():
    global options_list
    global spaces
    global used
    for item in range(NUMBER_OF_PAIRS):
        options_list.append(item)

    for item in range(CARD_COUNT):
        card = options_list[random.randint(0, len(options_list) - 1)]
        spaces.append(card)
        if card in used:
            used.remove(card)
            options_list.remove(card)
        else:
            used.append(card)


def update_checked_card(num, c_num):
    global correct
    col = num // GRID_HEIGHT
    row = num - (num // GRID_HEIGHT * GRID_HEIGHT)
    correct[row][col] = c_num


def is_match(first, second):
    global spaces
    global correct
    global matched_pairs
    global turns
    turns += 1
    if spaces[first] == spaces[second]:
        col_first = first // GRID_HEIGHT
        col_second = second // GRID_HEIGHT
        row_first = first - (first // GRID_HEIGHT * GRID_HEIGHT)
        row_second = second - (second // GRID_HEIGHT * GRID_HEIGHT)
        log_debug(f"CARD1: ({col_first}, {row_first})")
        log_debug(f"CARD2: ({col_second}, {row_second})")
        if correct[row_first][col_first] != 0 and correct[row_second][col_second] != 0:
            correct[row_first][col_first] = 1
            correct[row_second][col_second] = 1
            matched_pairs += 1
            return True
        if correct[row_first][col_first] == 2 and correct[row_second][col_second] == 2:
            correct[row_first][col_first] = 0
            correct[row_second][col_second] = 0
    return False


def restart_game():
    global options_list
    global used
    global spaces
    global new_grid
    global matched_pairs
    global first_guess
    global second_guess
    global correct
    global is_game_over
    global turns
    options_list = []
    used = []
    spaces = []
    new_grid = True
    turns = 0
    matched_pairs = 0
    first_guess = False
    second_guess = False
    correct = [[0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0]]
    is_game_over = False


# main game loop
running = True
while running:
    timer.tick(fps)
    screen.fill(Color.white.value)

    if new_grid is True:
        generate_grid()
        # spaces.sort()
        print(spaces)
        new_grid = False
    restart = draw_backgrounds()
    grid = draw_grid()

    if first_guess and second_guess:
        if is_match(first_guess_num, second_guess_num):
            pygame.mixer.Sound.play(match_sound_effect)
            log_debug("IT'S A MATCH")
        else:
            pygame.time.delay(1000)
            update_checked_card(first_guess_num, 0)
            update_checked_card(second_guess_num, 0)
        first_guess = False
        second_guess = False

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_j:
                for line in correct:
                    log_debug(line)
            if event.key == pygame.K_q:
                if not debug:
                    debug = True
                else:
                    debug = False

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(grid)):
                button = grid[i]
                if button.collidepoint(event.pos) and not first_guess:
                    first_guess = True
                    first_guess_num = i
                    log_debug(f"FIRST {i}")
                    update_checked_card(i, 2)
                if button.collidepoint(event.pos) and not second_guess and first_guess and first_guess_num != i:
                    second_guess = True
                    second_guess_num = i
                    log_debug(f"SECOND {i}")
                    update_checked_card(i, 2)
            if restart.collidepoint(event.pos):
                restart_var = True

    if first_guess:
        update_checked_card(first_guess_num, 2)

    if second_guess:
        update_checked_card(second_guess_num, 2)
    grid = draw_grid()

    if matched_pairs == NUMBER_OF_PAIRS:
        is_game_over = True
        winner = pygame.draw.rect(screen, Color.accent.value, [10, HEIGHT - 350, WIDTH - 20, 80], 0, 3)
        winner_text = title_font.render("You won! Great job!", True, Color.white.value)
        screen.blit(winner_text, (55, HEIGHT - 345))
    if restart_var:
        restart_game()
        restart_var = False

    pygame.display.flip()
pygame.quit()
