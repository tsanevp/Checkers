'''
Peter Tsanev
CS 5001, Fall 2021
This file is responsible for locating all the pieces of the current
player. It will allow us to determine all the playable moves the
player has. Everything is testable.
'''


class Player:
    '''
        Class -- Player
            The player of the game.
        Attributes:
            board -- An instance of the Board object.
        Methods:
            scan_for_piece -- Scans the board for the current player's
            pieces.
    '''

    def __init__(self, board):
        '''
            Constructor -- Creates a new instance of Player.
            Parameters:
                self -- The current Player object.
                board -- An instance of the Board object.
        '''
        self.board = board

    def scan_for_piece(self, turn):
        '''
            Method -- scan_for_piece
                Scans the board for the current player's pieces.
            Parameters:
                self -- The current Player object.
                turn -- Defines which player's turn it currently is.
            Returns:
                A list of indexes beloging to the pieces remaining on
                the board.
        '''
        piece = {}
        for index_row, row in enumerate(self.board.piece_location):
            for index_col, col in enumerate(row):
                if col != turn:
                    continue
                else:
                    piece[(index_row, index_col)] = turn
        self.player_pieces = list(piece.keys())
        return self.player_pieces
