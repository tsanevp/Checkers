from constants import BP, RP, EM, INITIAL_NUM_PIECES, INITIAL_NUM_KINGS
from board import Board


def test_constructor():
    board = Board()
    
    # Test number of pieces are called correctly
    black_left = board.black_left
    black_kings = board.black_kings
    assert(black_left == INITIAL_NUM_PIECES)
    assert(black_kings == INITIAL_NUM_KINGS)

    # Test defining and removing pieces work
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


def test_remove_checker():
    board = Board()
    # Initial board
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

    # Remove (0, 1) black piece
    board.remove_checker(0, 1)
    new_piece_locations = [
                           [EM, EM, EM, BP, EM, BP, EM, BP],
                           [BP, EM, BP, EM, BP, EM, BP, EM],
                           [EM, BP, EM, BP, EM, BP, EM, BP],
                           [EM, EM, EM, EM, EM, EM, EM, EM],
                           [EM, EM, EM, EM, EM, EM, EM, EM],
                           [RP, EM, RP, EM, RP, EM, RP, EM],
                           [EM, RP, EM, RP, EM, RP, EM, RP],
                           [RP, EM, RP, EM, RP, EM, RP, EM]
                          ]
    # Test to see if board gets updated
    assert(board.piece_location == new_piece_locations)
