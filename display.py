from createBoard import *

import os
import time
import math

import pygame
from pygame.transform import scale

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

main_resolution = (500, 500)
green = (63, 224, 87)
black = (14, 15, 18)
white = (255, 255, 255)
red = (255, 0, 0)
gra = (153, 255, 153)
grey = (100, 100, 100)

EMPTY = 0
GRASS = 1
TENT = 2
TREE = 3


def display(Board):

    pygame.init()
    window = pygame.display.set_mode(main_resolution)
    pygame.display.set_caption('SUDOKU')
    window.fill(white)

    board_size = len(Board[0])

    width, height = main_resolution
    offset = 50
    margin = 4
    cell_size = int((width - 2 * offset - (board_size - 1) * margin) / board_size)
    step = cell_size + 5
    font = pygame.font.SysFont("calibri", int(cell_size*2))

    coord_x = offset

    for y in range(board_size):
        coord_y = offset
        for x in range(board_size):
            cell = pygame.Rect(coord_x, coord_y, cell_size, cell_size)
            text = font.render(str(Board[x][y]), True, grey)
            window.blit(scale(text, (cell_size, cell_size)), cell)
            coord_y += step
        coord_x += step

    for x in range(offset, height - offset, step):
        for y in range(offset, width - offset, step):
            cell = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(window, green, cell, 1)

    start = offset + (cell_size // 4)
    stop = height - cell_size

    pygame.display.flip() 

    launched = True
    while launched:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                launched = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    launched = False
        time.sleep(0.1)