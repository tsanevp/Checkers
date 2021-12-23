from constants import BP, RP, EM
from board import Board
from game_state import GameState


def test_constructor():
    game = GameState()
    # Test each attribute
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
    assert(game.piece_location == piece_location)
    assert(game.turn == BP)
    assert(game.turn_count == 0)
    assert(game.skip_occured is False)
    assert(game.king is False)
    # Called within constructor
    click_postion = {-4: 0, -3: 1, -2: 2, -1: 3, 0: 4, 1: 5, 2: 6, 3: 7}
    assert(game.click_position == click_postion)
    # Called within constructor, move belongs to (2, 7) BP
    assert(game.valid_moves == {(3, 6): (2, 7)})
    assert(game.skipped == {})


def test_click_inbounds():
    game = GameState()
    assert(game.click_inbounds(-200, -200) is False)
    assert(game.click_inbounds(-200, 200) is False)
    assert(game.click_inbounds(200, -200) is False)
    assert(game.click_inbounds(200, 200) is False)
    assert(game.click_inbounds(-199, -199) is True)
    assert(game.click_inbounds(-199, 199) is True)
    assert(game.click_inbounds(199, -199) is True)
    assert(game.click_inbounds(199, 199) is True)
    assert(game.click_inbounds(0, 0) is True)


def test_contain_piece():
    game = GameState()
    game.contain_piece(0, 0)
    assert(game.selected_square == EM)
    game.contain_piece(0, 1)
    assert(game.selected_square == BP)
    game.contain_piece(4, 4)
    assert(game.selected_square == EM)
    game.contain_piece(5, 0)
    assert(game.selected_square == RP)


def test_scan_for_pieces():
    game = GameState()

    # Current turn is black
    game.scan_for_pieces()
    assert(game.valid_move_each_piece == [[{(3, 0): (2, 1), (3, 2): (2, 1)}],
                                          [{(3, 2): (2, 3), (3, 4): (2, 3)}],
                                          [{(3, 4): (2, 5), (3, 6): (2, 5)}],
                                          [{(3, 6): (2, 7)}]])
    assert(game.player_moves == [[{(3, 0): (2, 1), (3, 2): (2, 1)}],
                                 [{(3, 2): (2, 3), (3, 4): (2, 3)}],
                                 [{(3, 4): (2, 5), (3, 6): (2, 5)}],
                                 [{(3, 6): (2, 7)}]])
    assert(game.pieces == [(2, 1), (2, 1), (2, 3), (2, 3), (2, 5),
                           (2, 5), (2, 7)])

    # Current turn is red
    game.turn = RP
    game.scan_for_pieces()
    assert(game.valid_move_each_piece == [[{(4, 1): (5, 0)}],
                                          [{(4, 1): (5, 2), (4, 3): (5, 2)}],
                                          [{(4, 3): (5, 4), (4, 5): (5, 4)}],
                                          [{(4, 5): (5, 6), (4, 7): (5, 6)}]])
    assert(game.player_moves == [[{(4, 1): (5, 0)}],
                                 [{(4, 1): (5, 2), (4, 3): (5, 2)}],
                                 [{(4, 3): (5, 4), (4, 5): (5, 4)}],
                                 [{(4, 5): (5, 6), (4, 7): (5, 6)}]])
    assert(game.pieces == [(5, 0), (5, 2), (5, 2), (5, 4), (5, 4),
                           (5, 6), (5, 6)])


def test_possible_moves():  # Allows us to test traverse_left & traverse_right
    game = GameState()
    # Current turn is black
    # BP has no EM square to move to
    game.row_sel = 0
    game.col_sel = 1
    assert(game.possible_moves(0, 1) == {})
    # EM square, therefore nothing to move
    game.row_sel = 1
    game.col_sel = 2
    assert(game.possible_moves(1, 2) == {})
    # BP with EM square to move to
    game.row_sel = 2
    game.col_sel = 1
    assert(game.possible_moves(2, 1) == {(3, 0): (2, 1), (3, 2): (2, 1)})
    # Row, column out of index
    game.row_sel = 7
    game.col_sel = 10
    assert(game.possible_moves(7, 10) is False)

    # Current turn is red
    # RP has no EM square to move to
    game.turn = RP
    game.row_sel = 7
    game.col_sel = 0
    assert(game.possible_moves(7, 0) == {})
    # EM square, but per possible_moves has a "valid" move available
    game.row_sel = 6
    game.col_sel = 0
    assert(game.possible_moves(6, 0) == {(5, 1): (6, 0)})
    # RP with EM square to move to
    game.row_sel = 5
    game.col_sel = 0
    assert(game.possible_moves(5, 0) == {(4, 1): (5, 0)})
    # Row, column out of index
    game.row_sel = 7
    game.col_sel = 10
    assert(game.possible_moves(7, 10) is False)


def test_move_piece():
    game = GameState()
    board = Board()
    # Prior to change
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
    assert(game.piece_location == piece_location)
    # Move BP from (3, 0) to (4, 1)
    game.move_piece(2, 1, 3, 0)
    # New BP location
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
