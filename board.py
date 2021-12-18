'''
Peter Tsanev
CS 5001, Fall 2021
This board.py file is responsible for defining and setting up a board for
a game of checkers. This file handles everything related to Turtle and the UI
and is responsible for drawing the board, it's pieces, and performing pre-frame
updates. Only remove_checker and the class attributes are testable.
'''
import turtle
from checker import Checker
from constants import (NUM_SQUARES, SQUARE, SQUARE_COLORS, PIECE_ADJUSTMENTS,
                       RADIUS, BOARD_SIZE, WINDOW_SIZE, BOARD_CORNER, EM, BP,
                       RP, INITIAL_NUM_PIECES, INITIAL_NUM_KINGS)


class Board:
    '''
        Class -- Board
            The UI.
        Attributes:
            black_left = red_left -- The number of each piece remaining on
            the board.
            black_kings = red_kings -- The number of kings each player has.
            piece_location -- A nested list storing the location of each
            piece on the board.
            kings -- The location of king pieces on the board, if any.
        Methods:
            update_board -- Redraws the board squares and pieces.
            draw_valid_square_to_move -- Draws a blue outline on the
            squares the player has the option to move.
            draw_valid_move -- Draws the valid move options of a selected
            square.
            remove_checker -- Removes a checker from the board if skipped.
            winner -- Checks to see if a the game has a winner.
    '''

    def __init__(self):
        '''
            Constructor -- Creates a new instance of Board.
            Parameters:
                self -- The current Board object.
        '''
        self.black_left = self.red_left = INITIAL_NUM_PIECES
        self.black_kings = self.red_kings = INITIAL_NUM_KINGS
        # Piece location can be made into its own method in future.
        self.piece_location = [
                               [EM, BP, EM, BP, EM, BP, EM, BP],
                               [BP, EM, BP, EM, BP, EM, BP, EM],
                               [EM, BP, EM, BP, EM, BP, EM, BP],
                               [EM, EM, EM, EM, EM, EM, EM, EM],
                               [EM, EM, EM, EM, EM, EM, EM, EM],
                               [RP, EM, RP, EM, RP, EM, RP, EM],
                               [EM, RP, EM, RP, EM, RP, EM, RP],
                               [RP, EM, RP, EM, RP, EM, RP, EM]
                              ]
        self.kings = [[False for i in range(NUM_SQUARES)]
                      for i in range(NUM_SQUARES)]
        self.turtle_setup()
        self.init_board()
        self.update_board()

    def turtle_setup(self):
        '''
            Method -- turtle_setup
                Defines Turtle, creates the UI window, and defines the turtle
                pen to draw with.
            Parameters:
                self -- The current Board object.
        '''
        # Creates the UI window, which is the width of the board. It
        # includes a bit of margin... the + Square takes care of this.
        turtle.setup(WINDOW_SIZE, WINDOW_SIZE)

        # Sets the drawing canvas size, background color, appearance speed
        turtle.screensize(BOARD_SIZE, BOARD_SIZE)
        turtle.bgcolor(SQUARE_COLORS[1])
        turtle.tracer(0, 0)

        # Create the Turtle to draw board/pieces
        self.pen = turtle.Turtle()
        self.pen.penup()
        self.pen.hideturtle()
        self.pen.color("black", "white")

    def init_board(self):
        '''
            Method -- init_board
                Initializes and draws the board outline.
            Parameters:
                self -- The current Board object.
        '''
        self.draw_square(BOARD_CORNER, BOARD_CORNER, BOARD_SIZE)

    def update_board(self):
        '''
            Method -- update_board
                Makes any pre-frame updates to squares and checker pieces
                in regard to their current position.
            Parameters:
                self -- The current Board object.
        '''
        self.board_squares()
        self.draw_checkers()  # Each checker in current position

    def board_squares(self):
        '''
            Method -- board_squares
                Draws each checkered square on the board.
            Parameters:
                self -- The current Board object.
        '''
        self.pen.color("black", SQUARE_COLORS[0])
        for col in range(NUM_SQUARES):
            for row in range(NUM_SQUARES):
                if col % 2 != row % 2:
                    self.draw_square(BOARD_CORNER + SQUARE * row, BOARD_CORNER
                                     + SQUARE * col, SQUARE)

    def draw_square(self, row, col, size):
        '''
            Method -- draw_square
                Draw a square of a given size in the row and column passed.
            Parameters:
                self -- The current Board object.
                row -- The row to draw square in.
                col -- The column to draw the square in.
                size -- The size of the square to draw.
        '''
        RIGHT_ANGLE = 90
        self.pen.setposition(row, col)
        self.pen.begin_fill()
        self.pen.pendown()
        for i in range(4):
            self.pen.forward(size)
            self.pen.left(RIGHT_ANGLE)
        self.pen.penup()
        self.pen.end_fill()

    def draw_outline(self, row, col, size):
        '''
            Method -- draw_outline
                Draw an outline around a square given the row,
                column, and size.
            Parameters:
                self -- The current Board object.
                row -- The row to draw outline in.
                col -- The column to draw the outline in.
                size -- The size of the outline to draw.

        '''
        RIGHT_ANGLE = 90
        self.pen.setposition(row, col)
        self.pen.pendown()
        for i in range(4):
            self.pen.forward(size)
            self.pen.left(RIGHT_ANGLE)
        self.pen.penup()

    def draw_checkers(self):
        '''
            Method -- draw_checkers
                Draws the checkers in their current position on
                the board.
            Parameters:
                self -- The current Board object.
        '''
        for index_row, row in enumerate(self.piece_location):
            for index_col, col in enumerate(row):
                if col == "EMPTY":
                    continue
                elif col == "BLACK":
                    self.pen.color(col, col)
                elif col == "RED":
                    self.pen.color(col, col)
                self.pen.setposition(((BOARD_CORNER + SQUARE * index_col)
                                      + RADIUS, BOARD_CORNER + SQUARE
                                      * index_row + PIECE_ADJUSTMENTS))
                is_king = self.kings[index_row][index_col]
                Checker(self.pen, is_king)

    def draw_valid_move(self, moves):
        '''
            Method -- draw_valid_move
                Draws the valid moves of a selected piece, if any. This
                entails outlining the squares in red that are considered
                a valid move.
            Parameters:
                self -- The current Board object.
                moves -- A dictionary containing valid moves the player
                can make.
        '''
        for move in moves:
            self.pen.color("red")
            self.draw_outline(BOARD_CORNER + SQUARE * move[1], BOARD_CORNER
                              + SQUARE * move[0], SQUARE)

    def draw_valid_square_to_move(self, selected):
        '''
            Method -- draw_valid_square_to_move
                Draws a blue outline around squares that the player has
                the option to move.
            Parameters:
                self -- The current Board object.
                selected -- The (row, column) of a square that can be moved.
        '''
        self.pen.color("blue")
        self.draw_outline(BOARD_CORNER + SQUARE * selected[1], BOARD_CORNER
                          + SQUARE * selected[0], SQUARE)

    def remove_checker(self, row, col):
        '''
            Method -- remove_checker
                Removes the checker in the given row and column from the
                checker board.
            Parameters:
                self -- The current Board object.
                row -- The row the checker is in.
                col -- The column the checker is in.
        '''
        skipped = self.piece_location[row][col]
        if skipped == BP:
            self.black_left -= 1
        elif skipped == RP:
            self.red_left -= 1
        self.piece_location[row][col] = EM

    def winner(self, turn, player_moves, turn_count, winner=None):
        '''
            Method -- winner
                Checks to see if a player has won. Decision based on the number
                of each color's remaining pieces, and if the current player
                has any valid moves.
            Parameters:
                self -- The current Board object.
                turn -- Defines whose turn it currently is.
                player_moves -- A dictionary of moves the player can make.
                turn_count -- The number of turns made since the game started.
        '''
        if turn_count > 0:
            if self.black_left <= 0 or (turn == RP and len(player_moves) == 0):
                winner = RP

            if self.red_left <= 0 or (turn == BP and len(player_moves) == 0):
                winner = BP

        self.game_over(winner)

    def game_over(self, winner):
        '''
            Method -- game_over
                If there is a winner, prints that the game has ended along with
                the winning player's color on the UI screen.
            Parameters:
                self -- The current Board object.
                winner -- The winner of the game.
        '''
        if winner is not None:
            self.pen.color("BLUE")
            self.pen.setposition(BOARD_CORNER*3/4 + 10, -40)
            self.pen.write("GAME OVER!\n{} wins!".format(winner.lower()),
                           font=("Verdana", 40, "normal"))
