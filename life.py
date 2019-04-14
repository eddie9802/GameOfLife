import numpy as np
from copy import copy, deepcopy
import time
import os
import pygame

BOARDSIZE = 48
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
WIDTH = 20
HEIGHT = 20
MARGIN = 1

pygame.init()
 
# Set the width and height of the screen [width, height]
WINDOW_SIZE = [1008, 1008]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
pygame.display.set_caption("Game Of Life")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

def createBoard():
    board = [[0 for i in range(0, BOARDSIZE)] for j in range(0, BOARDSIZE)]
    board[2][0] = 1
    board[2][1] = 1
    board[2][2] = 1
    board[1][2] = 1
    board[0][1] = 1
    return board

def findNNeighbours(board, pos):
    checkColAhead = 0
    checkRowAhead = 0
    nNeighBours = 0
    if pos["row"] > 0:
        curRow = pos["row"] - 1
    else:
        curRow = pos["row"]
    if pos["col"] > 0:
        curCol = pos["col"] - 1
    else:
        curCol = pos["col"]
    if pos["col"] < BOARDSIZE - 1:
        checkColAhead = 2
    else:
        checkColAhead = 1
    if pos["row"] < BOARDSIZE - 1:
        checkRowAhead = 2
    else:
        checkRowAhead = 1
    for i in range(curRow, pos["row"] + checkRowAhead):
        for j in range(curCol, pos["col"] + checkColAhead):
            if board[i][j] == 1 and (pos["row"] != i or pos["col"] != j):
                nNeighBours = nNeighBours + 1



    return nNeighBours

def getNextState(cellAlive, nNeighbours):
    if not cellAlive and nNeighbours == 3:
        return 1
    if cellAlive and (nNeighbours == 2 or nNeighbours == 3):
        return 1
    else:
        return 0

def propagateGen(board):
    copyBoard = deepcopy(board)
    for row in range(0, BOARDSIZE):
        for col in range(0, BOARDSIZE):
            pos = {"row": row, "col": col}
            cellAlive = False
            if copyBoard[row][col] == 1:
                cellAlive = True
            nNeighbours = findNNeighbours(copyBoard, pos)
            board[row][col] = getNextState(cellAlive, nNeighbours)
    return board

def drawBoard(board):
    screen.fill(BLACK)
    for row in range(BOARDSIZE):
        for column in range(BOARDSIZE):
            color = WHITE
            if board[row][column] == 1:
                color = GREEN
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
    pygame.display.flip()

if __name__=='__main__':
    board = createBoard()
    paused = False
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                # Set that location to one
                board[row][column] = 1
            elif event.type == pygame.KEYDOWN:
                if event.key == ord(" ") and not paused:
                    paused = True
                elif event.key == ord(" ") and paused:
                    paused = False
                elif event.key == ord("r"):
                    board = [[0 for i in range(0, BOARDSIZE)] for j in range(0, BOARDSIZE)]
                    paused = True
                elif event.key == ord("1"):
                    board = propagateGen(board)
                    paused = True
        if not paused:
            board = propagateGen(board)
            time.sleep(0.1)
        drawBoard(board)
    pygame.quit()
    
    