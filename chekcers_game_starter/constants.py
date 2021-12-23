'''
Peter Tsanev
CS 5001, Fall 2021
This python file holds all the constants that will be used
in the checkers program. It will allows the program to call
specific constants within each class.
'''

# Board constants
NUM_SQUARES = 8
SQUARE = 50
BOARD_SIZE = NUM_SQUARES * SQUARE
WINDOW_SIZE = BOARD_SIZE + SQUARE
BOARD_CORNER = -BOARD_SIZE / 2 - 1
LOW_BOUNDS = -BOARD_SIZE / 2
UPPER_BOUNDS = BOARD_SIZE / 2

# Checker piece constants
RADIUS = SQUARE / 2
PIECE_ADJUSTMENTS = 1
SQUARE_COLORS = ("light gray", "white")
BP = "BLACK"
RP = "RED"
EM = "EMPTY"
INITIAL_NUM_PIECES = 12
INITIAL_NUM_KINGS = 0
