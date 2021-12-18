from constants import BP, RP, EM
from board import Board
from checker import Checker


def test_constructor():
    # Checks if (0, 1) black piece is a king
    board = Board()
    is_king = board.kings[0][1]

    checker = Checker(board.pen, is_king)
    assert(checker.is_king is False)

    # Change (0, 1) black piece to king
    board.kings[0][1] = True
    is_king = board.kings[0][1]

    checker = Checker(board.pen, is_king)
    assert(checker.is_king is True)
