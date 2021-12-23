from constants import BP, RP, EM
from board import Board
from player import Player


def test_constructor():
    board = Board()
    player = Player(board)

    # Initial piece positions
    piece_location = [
                      [EM, BP, EM, BP, EM, BP, EM, BP],
                      [BP, EM, BP, EM, BP, EM, BP, EM],
                      [EM, BP, EM, BP, EM, BP, EM, BP],
                      [EM, EM, EM, EM, EM, EM, EM, EM],
                      [EM, EM, EM, EM, EM, EM, EM, EM],
                      [RP, EM, RP, EM, RP, EM, RP, EM],
                      [EM, RP, EM, RP, EM, RP, EM, RP],
                      [RP, EM, RP, EM, RP, EM, RP, EM]
                     ]
    assert(board.piece_location == piece_location)


def test_scan_for_piece():
    board = Board()
    player = Player(board)

    # Based on initial piece positions
    turn_black = player.scan_for_piece(BP)
    turn_red = player.scan_for_piece(RP)
    assert(turn_black == [(0, 1), (0, 3), (0, 5), (0, 7), (1, 0), (1, 2),
                          (1, 4), (1, 6), (2, 1), (2, 3), (2, 5), (2, 7)])
    assert(turn_red == [(5, 0), (5, 2), (5, 4), (5, 6), (6, 1), (6, 3),
                        (6, 5), (6, 7), (7, 0), (7, 2), (7, 4), (7, 6)])
