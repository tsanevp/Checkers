'''
Peter Tsanev
CS 5001, Fall 2021
This file handles everything related to the game state as well as all logic. To
test this file, lines 50-52 must be commented out.
'''
from constants import NUM_SQUARES, SQUARE, BP, RP, EM, LOW_BOUNDS, UPPER_BOUNDS
from board import Board
import turtle
from player import Player
import random


class GameState:
    '''
        Class -- GameState
            The state of the game.
        Attributes:
            board -- A Board object used to keep track of piece locations
            and to update game as moves are made.
            piece_location -- A nested list storing the location of each
            piece on the board.
            player -- A Player object used to find the row and column of
            the current player's pieces on the board.
            turn -- Defines the player whose turn is first.
            turn_count -- The starting number of turns player thus far.
            skip_occured -- Defines if a skip was made when a piece is
            moved.
            king -- Defines if a piece as a king.
            click_position -- A dictionary used to determine the row and
            column a click was made in. Required since our lower bounds
            are negative.
            valid_moves -- A dictionary that stores valid moves the
            current player can make.
            skipped -- A dictionary that stores the locations of the
            pieces that can be skipped.
            screen -- The Turtle UI screen.
        Methods:
            (none intended to be accessed outside the class)
    '''

    def __init__(self):
        '''
            Constructor -- Creates a new instance of GameState.
            Parameters:
                self -- The current GameState object.
        '''
        self._init_game()

        self.screen = turtle.Screen()
        self.screen.onclick(self.board_click)
        turtle.done()

    def _init_game(self):
        '''
            Method -- _init_game
                A private method. Initializes the current GameState object
                with inital conditions defined below.
            Parameters:
                self -- The current GameState object.
        '''
        self.board = Board()
        self.piece_location = self.board.piece_location
        self.player = Player(self.board)
        self.selected = False
        self.turn = BP
        self.turn_count = 0
        self.skip_occured = False
        self.king = None
        self.click_position = self.valid_moves = self.skipped = {}
        self.click_row_col()
        self.scan_for_pieces()
        self.board.current_turn(self.turn)
        self.board.black_pieces_left()
        self.board.red_pieces_left()

    def click_row_col(self):
        '''
            Method -- click_row_col
                Creates a dictionary that is used to determine what row/colomn
                the user click is in.
            Parameters:
                self -- The current GameState object.
            Returns:
                A dictionary whose key is the click location made on the board,
                and the value is the row/column the click made is in.
        '''
        j = 0
        for i in range(int(-NUM_SQUARES/2), int(NUM_SQUARES/2)):
            self.click_position[i] = j
            j += 1
        return self.click_position

    def board_click(self, x, y):
        '''
            Method -- board_click
                Called when a click occurs. Only has effect if the current
                player is black.
            Parameters:
                self -- The current GameState object.
                x -- X coordinate of click. Automatically provided by Turtle.
                y -- Y coordinate of click. Automatically provided by Turtle.
        '''
        if self.turn == BP:
            if self.click_inbounds(x, y):  # Checks click inbounds
                self.row_sel = self.click_position[y // SQUARE]  # Row selected
                self.col_sel = self.click_position[x // SQUARE]  # Col selected

                # Updates the UI with each click made
                self.board.update_board()
                self.outline_square_w_movable_piece()

                # If a black piece is selected, control and move piece
                self.contain_piece(self.row_sel, self.col_sel)
                self.select(self.row_sel, self.col_sel)

    def click_inbounds(self, x, y):
        '''
            Method -- click_inbounds
                Determines if the click is within the bounds of   the board.
            Parameters:
                self -- The current GameState object.
                x -- The x-coordinate of the click.
                y -- The y-coordinate of the click.
            Returns:
                True if in-bounds, False otherwise.
        '''
        return (x > LOW_BOUNDS and x < UPPER_BOUNDS)\
            and (y > LOW_BOUNDS and y < UPPER_BOUNDS)

    def contain_piece(self, row, col):
        '''
        Method -- contain_piece
            Determines if the square clicked on contains a piece. If it
            does, returns the piece (row, col).
        Parameters:
                self -- The current GameState object.
        Returns:
            The row and column of the selected piece as a list.
        '''
        # Determines if the selected square contains a piece
        self.selected_square = (self.piece_location[row][col])
        self.selected_piece = [row, col]
        return self.selected_piece

    def scan_for_pieces(self):
        '''
            Method -- scan_for_pieces
                Scans the board for the current players pieces and creates
                and list of each piece's row and column. It then passes
                that list to scan_for_moves.
            Parameters:
                self -- The current GameState object.
        '''
        self.each_piece_location = self.player.scan_for_piece(self.turn)
        self.scan_for_moves(self.each_piece_location)

    def scan_for_moves(self, each_piece_location):
        '''
            Method -- scan_for_moves
                Uses the list of each piece's row and column to determine
                if each piece has any valid moves or skip moves. If yes,
                appends them to a new, nested list.
                (eg. list = [[{valid_moves}, {skip_moves}], [...], ...])
            Parameters:
                self -- The current GameState object.
                each_piece_location -- A list with the location of each piece
                on the board.
        '''
        self.valid_move_each_piece = []
        for piece in each_piece_location:
            self.row_sel = piece[0]
            self.col_sel = piece[1]
            # Both methods called for each individual piece location
            self.contain_piece(self.row_sel, self.col_sel)
            self.moves_of_piece(self.row_sel, self.col_sel)

        # Finalizes possibles moves and draws outline around movable checkers
        self.moves_to_make(self.valid_move_each_piece)

    def moves_of_piece(self, row, col):
        '''
            Method -- moves_of_piece
                Iteratively finds all the possible moves of each piece
                remaining on the board and appends them to a list. If
                for a given piece there are no valid moves, returns,
                and moves to next piece.
            Parameters:
                self -- The current GameState object.
                row -- The row of current piece.
                col -- The column of current piece.
        '''
        moves_wo_skip = []
        self.valid_moves = self.possible_moves(row, col)

        # Removes any normal moves if a piece has a skip move
        if len(self.skipped) > 0:
            for key in self.valid_moves:
                if key not in self.skipped:
                    moves_wo_skip.append(key)
            for move in moves_wo_skip:
                self.valid_moves.pop(move)

        if len(self.valid_moves) == 0:
            return

        # Appends a list of two dict [{valid moves}, {skip moves}] to a list
        self.valid_move_each_piece.append([self.valid_moves, self.skipped])

    def moves_to_make(self, player_moves):
        '''
            Method -- moves_to_make
                If a skippable move tied to a piece is present, removes the
                valid moves of all other pieces. Also, checks if the current
                player has any valid moves. After, creates a list of square
                locations that contain playable pieces.
            Parameters:
                self -- The current GameState object.
                player_moves -- A nest list, where each index is a list
                of two dictionaries related to each movable piece. The first
                is all valid moves, and the second is all skippable pieces.
        '''
        moves_with_skips = []
        # If skip move is possible, removes other non-skip moves
        for valid_moves in player_moves:
            if len(valid_moves[-1]) != 0:
                moves_with_skips.append(valid_moves)
                self.skip_occured = True
            else:
                valid_moves.remove(valid_moves[-1])

        # Reassigns original list of valid moves to list with only skip moves
        if len(moves_with_skips) != 0:
            player_moves = moves_with_skips
        elif self.skip_occured:
            player_moves = {}

        # If the current player has no valid moves, switches turns
        if len(player_moves) == 0:
            self.switch_turns()

        # Finds the row and column of the pieces with valid moves
        self.player_moves = player_moves
        self.pieces = []
        for lst in player_moves:
            for key in lst[0]:
                piece = lst[0][key]
                self.pieces.append(piece)
        if self.turn == BP:
            self.outline_square_w_movable_piece()

    def outline_square_w_movable_piece(self):
        '''
            Method -- outline_squares_w_movable_piece
                Draws a blue outline around any squares that contain
                a piece with a playable move.
        '''
        for piece in self.pieces:
            self.board.draw_valid_square_to_move(piece)

    def select(self, row, col):  # selecting the piece you wish to move
        '''
            Method -- select
                Allows the human player to select the piece they wish to move.
                If the selected piece has any playable moves, outlines the
                square location each move in red on the screen. If while still
                selected a outlined square is clicked, moves the selected piece
                there.
            Parameters:
                self -- The current GameState object.
                row -- Row belonging to the currently selected square.
                col -- Column belonging to currently selected square.
            Returns:
                If each user click satisfies the defined logic, a piece is
                moved and the turn is switched. Else, returns False.
        '''
        moves_wo_skip = []
        # Moves piece if criteria below met
        if self.selected:
            self.move(row, col)
        if self.turn == RP:
            return
        piece = self.selected_square
        self.piece_row = row
        self.piece_col = col

        # Checks to see if selected piece meets criteria to be moved
        if piece != EM and piece == self.turn and (row, col) in self.pieces:
            self.valid_moves = self.possible_moves(row, col)

            # Removes and moves w/o skips, if appliable
            if len(self.skipped) > 0:
                for key in self.valid_moves:
                    if key not in self.skipped:
                        moves_wo_skip.append(key)
                for move in moves_wo_skip:
                    self.valid_moves.pop(move)

            # Draws valid moves for selected piece
            self.board.draw_valid_move(self.valid_moves)
            self.selected = True
        else:
            self.selected = False
            return False

    def move(self, row, col):
        '''
            Method -- move
                Moves the selected player piece to the choosen square.
            Parameters:
                self -- The current GameState object.
                row -- Row to move the piece to.
                col -- Column to move the piece to.
        '''
        # If the select sqare is empty and in valid moves, moves the piece
        piece = self.selected_square
        if piece == EM and (row, col) in self.valid_moves:
            self.move_piece(self.piece_row, self.piece_col, row, col)

            # If a skip move is made, removes piece skipped
            self.remove_checker((row, col))

            # If skip made, checks if new row/col has possible skip moves
            self.possible_moves(row, col)
            if len(self.skipped) == 0:
                self.skip_occured = False
            self.board.update_board()

            # Allow player to keep capturing pieces if applicable
            if self.skip_occured:
                self.scan_for_moves([(row, col)])
                return self.screen.onclick(self.board_click)

            # Switch turns once a normal or multiple piece capture move made
            self.switch_turns()
            if self.turn == RP:
                self.turn_ai()

    def turn_ai(self):
        '''
            Method -- turn_ai
                Is called is player turn is RED. Controls and calls all of the
                ai methods.
            Parameters:
                self -- The current GameState object.
        '''
        self.scan_for_pieces()  # Finds possible moves of all ai pieces
        self.screen.ontimer(self.move_ai, 1000)  # Delays ai moves

    def move_ai(self):
        '''
            Method -- move_ai
                Moves the ai pieces. Prioritizes skip moves over
                standard moves. If multiple skip or if multiple noraml
                moves available, will randomly select a move to make.
            Parameters:
                self -- The current GameState object.
        '''
        rand_move_keys = []
        # Ensures there is playable move, if not, switches turns
        if len(self.player_moves) > 0:
            if self.skip_occured:
                # Runs if skip move available
                ai_rand_move = random.choice(self.player_moves)
                rand_move_keys.append(list(ai_rand_move[0].keys()))
                rand_move_keys = [i[0] for i in rand_move_keys]
                ai_move = random.choice(rand_move_keys)
                skip_row = ai_rand_move[1][ai_move][0]
                skip_col = ai_rand_move[1][ai_move][1]

                # If a piece is skipped, remove it
                self.remove_checker((skip_row, skip_col))
            else:
                # Runs if only standard moves available
                ai_rand_move = random.choice(self.player_moves)
                for dict in ai_rand_move:
                    rand_move_keys.append(list(dict.keys()))
                rand_move_keys = [i[0] for i in rand_move_keys]
                ai_move = random.choice(rand_move_keys)

            # Defines piece row/column and row/column to move to
            piece_row = ai_rand_move[0][ai_move][0]
            piece_col = ai_rand_move[0][ai_move][1]
            new_row = ai_move[0]
            new_col = ai_move[1]

            # Moves the current piece to new location
            self.move_piece(piece_row, piece_col, new_row, new_col)

            # If skip made, checks if new row/col has possible skip moves
            self.possible_moves(new_row, new_col)
            if len(self.skipped) == 0:
                self.skip_occured = False
            self.board.update_board()

            # Allow ai to keep capturing pieces if applicable
            if self.skip_occured:
                self.scan_for_moves([(new_row, new_col)])
                return self.screen.ontimer(self.move_ai, 1000)

            # Switch turns once a normal or multiple piece capture move made
            self.switch_turns()
            self.scan_for_pieces()
        else:
            self.switch_turns()

    def possible_moves(self, row, col):
        '''
            Method -- possible_moves
                Determines playable standard and skip moves for each player.
            Parameters:
                self -- The current GameState object.
                row -- Row belonging to the currently selected piece.
                col -- Column belonging to the currently selected piece.
            Returns:
                Possible moves of selected piece as a dictionary.
        '''
        self.skipped = {}
        moves = {}
        left = col - 1
        right = col + 1
        self.row = row
        try:
            self.king = self.board.kings[row][col]
            if self.turn == BP or self.king:
                moves_row = row + 1
                moves.update(self.traverse_left(1, left, moves_row))
                moves.update(self.traverse_right(1, right, moves_row))
            if self.turn == RP or self.king:
                moves_row = row - 1
                moves.update(self.traverse_left(-1, left, moves_row))
                moves.update(self.traverse_right(-1, right, moves_row))
            return moves
        except IndexError:
            return False

    def traverse_left(self, step, left, row, skipped=[], piece_color=None):
        '''
            Method -- traverse_left
                Determines if the selected piece can move to the left,
                diagonally adjacent square or if the piece can skip another.
            Parameters:
                self -- The current GameState object.
                step -- Defines the direction the piece is moving in.
                left -- Looks for valid moves one column to the left.
                row -- Looks for valid moves in the defined row.
                skipped -- A list of skipped pieces (row, col).
                piece_color -- Color of the piece not currently being moved.
            Returns:
                A dictionary containing the valid moves of the piece.
        '''
        moves = {}
        skipped_piece = {}
        # Checks to make sure row/column of next square are in bounds
        if left <= -1 or left >= NUM_SQUARES or row < 0\
                or row > 7 or skipped == EM:
            return moves

        # Returns moves if next square contains piece of current player
        current = self.piece_location[row][left]
        if current == piece_color:
            return moves

        last = (row, left)
        if step == 1:
            new_row = row + 1
        else:
            new_row = row - 1

        # Valid moved stored if next square is empty
        if current == EM:
            if len(skipped) != 0:
                skipped_piece[(row, left)] = skipped
                self.skipped.update(skipped_piece)
            moves[(row, left)] = (self.row_sel, self.col_sel)

        # If not empty and occupied by opposite player, check if can skip
        if current != EM and self.turn != current:
            moves.update(self.traverse_left(step, left-1, new_row,
                                            skipped=last, piece_color=current))
        return moves

    def traverse_right(self, step, right, row, skipped=[], piece_color=None):
        '''
            Method -- traverse_right
                Determines if the selected piece can move to the right,
                diagonally adjacent square of if the piece can skip another.
            Parameters:
                self -- The current GameState object.
                step -- Defines the direction the piece is moving in.
                right -- Looks for valid moves one column to the right.
                row -- Looks for valid moves in the defined row.
                skipped -- A list of skipped pieces (row, col).
                piece_color -- Color of the piece not currently being moved.
            Returns:
                A dictionary containing the valid moves of the piece.
        '''
        moves = {}
        skipped_piece = {}
        # Checks to make sure row/column of next square are in bounds
        if right >= NUM_SQUARES or right <= -1 or row < 0\
                or row >= NUM_SQUARES or skipped == EM:
            return moves

        # Returns moves if next square contains piece of current player
        current = self.piece_location[row][right]
        if current == piece_color:
            return moves

        last = (row, right)
        if step == 1:
            new_row = row + 1
        else:
            new_row = row - 1

        # Valid moved stored if next square is empty
        if current == EM:
            if len(skipped) != 0:
                skipped_piece[(row, right)] = skipped
                self.skipped.update(skipped_piece)
            moves[(row, right)] = (self.row_sel, self.col_sel)

        # If not empty and occupied by opposite player, check if can skip
        if current != EM and self.turn != current:
            moves.update(self.traverse_right(step, right+1, new_row,
                                             skipped=last,
                                             piece_color=current))
        return moves

    def move_piece(self, piece_row, piece_col, row, col):
        '''
            Method -- move_piece
                Moves the selected piece to another square by changing
                nested list of checker locations.
            Parameters:
                self -- The current GameState object.
                piece_row -- The row of the piece intended to be moved.
                piece_col -- The column of the piece intended to be moved.
                row -- The row to move the piece to.
                col -- The column to move the piece to.
        '''
        # Moves the piece within the nested list containing piece locations
        (self.piece_location[piece_row][piece_col],
         self.piece_location[row][col]) = \
            (self.piece_location[row][col],
             self.piece_location[piece_row][piece_col])

        # Keeps track of which pieces are kings, and if the king is being moved
        (self.board.kings[piece_row][piece_col],
         self.board.kings[row][col]) = \
            (self.board.kings[row][col],
             self.board.kings[piece_row][piece_col])

        # Converts piece to King if it reaches opposite side
        if row == NUM_SQUARES - 1 or row == 0:
            self.board.kings[row][col] = self.is_king()
            if self.turn == BP:
                self.board.black_kings += 1
            else:
                self.board.red_kings += 1

    def switch_turns(self):
        '''
            Method -- switch_turnss
                When this method is called, the player turns switch.
                Then checks to see if the game is over.
            Parameters:
                self -- The current GameState object.
        '''
        if self.turn == "BLACK":
            self.turn = "RED"
        else:
            self.turn = "BLACK"
        self.turn_count += 1

        # Displays whose turn it currently is
        self.board.current_turn(self.turn)
        self.board.black_pieces_left()
        self.board.red_pieces_left()
 
        # Checks to see if game has ended
        self.board.winner(self.turn, self.player_moves, self.turn_count)

    def remove_checker(self, skipped):
        '''
            Method -- remove_checker
                Removes the checker that was skipped.
            Parameters:
                self -- The current GameState object.
                skipped -- The (row, column) of the skipped piece.
        '''
        if self.turn == RP:
            # If skipped piece is a king, reassigns is.king to False
            self.board.kings[skipped[0]][skipped[1]] = False
            self.board.remove_checker(skipped[0], skipped[1])
        else:
            # Checks if skipped piece is in the dictionary of skippable pieces
            if skipped in self.skipped:
                skipped_piece = self.skipped[skipped]
                self.board.kings[skipped_piece[0]][skipped_piece[1]] = False
                self.board.remove_checker(skipped_piece[0], skipped_piece[1])

    def is_king(self):
        '''
            Method -- is_king
                Defines the current piece as a king.
            Parameters:
                self -- The current GameState object.
            Returns:
                True.
        '''
        return True
