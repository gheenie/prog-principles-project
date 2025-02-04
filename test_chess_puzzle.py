from copy import deepcopy

from chess_puzzle import *

import pytest


def test_locatio2index1():
    assert location2index("e2") == (5,2)


def test_location2index_row_is_double_digit():
    assert location2index('g10') == (7, 10)
    assert location2index('z26') == (26, 26)


def test_location2index_input_is_not_string():
    with pytest.raises(TypeError) as e:
        location2index(52)
    assert str(e.value) == 'Location is not a string.'
    with pytest.raises(TypeError) as e:
        location2index(['e2'])
    assert str(e.value) == 'Location is not a string.'


def test_location2index_input_is_empty_string():
    with pytest.raises(ValueError) as e:
        location2index('')
    assert str(e.value) == 'Location is empty.'


def test_location2index_column_is_out_of_bounds():
    # Integer.
    with pytest.raises(ValueError) as e:
        location2index('55')
    assert str(e.value) == 'Column is out of the range of characters a to z.'
    with pytest.raises(ValueError) as e:
        location2index('526')
    assert str(e.value) == 'Column is out of the range of characters a to z.'
    # Capital letter.
    with pytest.raises(ValueError) as e:
        location2index('A5')
    assert str(e.value) == 'Column is out of the range of characters a to z.'
    # Character that isn't a letter.
    with pytest.raises(ValueError) as e:
        location2index('#26')
    assert str(e.value) == 'Column is out of the range of characters a to z.'


def test_location2index_row_is_invalid():
    with pytest.raises(ValueError) as e:
        location2index('ee')
    assert str(e.value) == 'Row is incorrectly formatted.'
    with pytest.raises(ValueError) as e:
        location2index('zz')
    assert str(e.value) == 'Row is incorrectly formatted.'


def test_location2index_row_out_of_bounds():
    with pytest.raises(ValueError) as e:
        location2index('z27')
    assert str(e.value) == 'The row is out of bounds.'
    with pytest.raises(ValueError) as e:
        location2index('a0')
    assert str(e.value) == 'The row is out of bounds.'
    with pytest.raises(ValueError) as e:
        location2index('m-1')
    assert str(e.value) == 'The row is out of bounds.'


def test_index2location1():
    assert index2location(5,2) == "e2"


def test_index2location_row_is_double_digit():
    assert index2location(5, 20) == "e20"
    assert index2location(26, 26) == "z26"


def test_index2location_input_is_not_ints():
    with pytest.raises(TypeError) as e:
        index2location(5, [2])
    assert str(e.value) == 'One of the indices is not an integer.'
    with pytest.raises(TypeError) as e:
        index2location('5', 2)
    assert str(e.value) == 'One of the indices is not an integer.'


def test_index2location_column_out_of_bounds():
    with pytest.raises(ValueError) as e:
        index2location(27, 26)
    assert str(e.value) == 'The column is out of bounds.'
    with pytest.raises(ValueError) as e:
        index2location(0, 1)
    assert str(e.value) == 'The column is out of bounds.'
    with pytest.raises(ValueError) as e:
        index2location(-1, 2)
    assert str(e.value) == 'The column is out of bounds.'


def test_index2location_row_out_of_bounds():
    with pytest.raises(ValueError) as e:
        index2location(26, 27)
    assert str(e.value) == 'The row is out of bounds.'
    with pytest.raises(ValueError) as e:
        index2location(1, 0)
    assert str(e.value) == 'The row is out of bounds.'
    with pytest.raises(ValueError) as e:
        index2location(2, -1)
    assert str(e.value) == 'The row is out of bounds.'


wn1 = Knight(1,2,True)
wn2 = Knight(5,2,True)
wn3 = Knight(5,4, True)
wk1 = King(3,5, True)

bn1 = Knight(1,1,False)
bk1 = King(2,3, False)
bn2 = Knight(2,4, False)

B1 = (5, [wn1, bn1, wn2, bn2, wn3, wk1, bk1])
'''
  ♔  
 ♞  ♘
 ♚   
♘   ♘
♞    
'''


def test_is_piece_at1():
    assert is_piece_at(2,2, B1) == False


@pytest.fixture(scope="function")
def board1():
    '''
      ♔  
     ♞  ♘
     ♚   
    ♘   ♘
    ♞    
    '''
    wn12 = Knight(1, 2, True)
    wn52 = Knight(5, 2, True)
    wn54 = Knight(5, 4, True)
    wk35 = King(3, 5, True)
    bn11 = Knight(1, 1, False)
    bn24 = Knight(2, 4, False)
    bk23 = King(2, 3, False)

    return (5, [wn12, wn52, wn54, wk35, bn11, bn24, bk23])


def test_is_piece_at_is_true_for_any_white_pieces(board1):
    assert is_piece_at(1, 2, board1) is True
    assert is_piece_at(5, 2, board1) is True
    assert is_piece_at(5, 4, board1) is True
    assert is_piece_at(3, 5, board1) is True


def test_is_piece_at_is_true_for_any_black_pieces(board1):
    assert is_piece_at(1, 1, board1) is True
    assert is_piece_at(2, 3, board1) is True
    assert is_piece_at(2, 4, board1) is True


def test_is_piece_at_column_out_of_bounds(board1):
    with pytest.raises(ValueError) as e:
        is_piece_at(7, 1, board1)
    assert str(e.value) == 'One of the coordinate is out of bounds.'
    with pytest.raises(ValueError) as e:
        is_piece_at(0, 5, board1)
    assert str(e.value) == 'One of the coordinate is out of bounds.'


def test_is_piece_at_row_out_of_bounds(board1):
    with pytest.raises(ValueError) as e:
        is_piece_at(1, 6, board1)
    assert str(e.value) == 'One of the coordinate is out of bounds.'
    with pytest.raises(ValueError) as e:
        is_piece_at(5, -1, board1)
    assert str(e.value) == 'One of the coordinate is out of bounds.'


def test_piece_at1():
    assert piece_at(1,1, B1) == bn1


def test_piece_at_white_knight(board1):
    result_piece = piece_at(1, 2, board1)

    assert result_piece is board1[1][0]


def test_piece_at_white_king(board1):
    result_piece = piece_at(3, 5, board1)

    assert result_piece is board1[1][3]


def test_piece_at_black_knight(board1):
    result_piece = piece_at(2, 4, board1)

    assert result_piece is board1[1][5]


def test_piece_at_black_king(board1):
    result_piece = piece_at(2, 3, board1)

    assert result_piece is board1[1][6]


def test_can_reach1():
    assert bn1.can_reach(2,2, B1) == False


@pytest.fixture(scope="function")
def board2():
    '''
     ♘♔  
     ♞ ♘♘
     ♚ ♞ 
    ♘ ♞ ♘
    ♞    
    '''
    wn12 = Knight(1, 2, True)
    wn52 = Knight(5, 2, True)
    wn54 = Knight(5, 4, True)
    wn44 = Knight(4, 4, True)
    wn25 = Knight(2, 5, True)
    wk35 = King(3, 5, True)
    bn11 = Knight(1, 1, False)
    bn24 = Knight(2, 4, False)
    bn32 = Knight(3, 2, False)
    bn43 = Knight(4, 3, False)
    bk23 = King(2, 3, False)

    return (5, [wn12, wn52, wn54, wn44, wn25, wk35, bn11, bn24, bn32, bn43, bk23])
    

def test_can_reach_knight_valid_movement_and_no_same_side_piece(board1, board2):
    wn12 = piece_at(1, 2, board1)
    wn52 = piece_at(5, 2, board1)
    bn11 = piece_at(1, 1, board1)
    bn24 = piece_at(2, 4, board1)
    wn44 = piece_at(4, 4, board2)
    bn43 = piece_at(4, 3, board2)

    # Landing on opponent knight.
    assert wn12.can_reach(2, 4, board1) is True
    assert bn24.can_reach(1, 2, board1) is True
    # Landing on empty space.
    assert wn52.can_reach(3, 3, board1) is True
    assert bn11.can_reach(3, 2, board1) is True
    # Landing on opponent king.
    assert wn44.can_reach(2, 3, board2) is True
    assert bn43.can_reach(3, 5, board2) is True


def test_can_reach_knight_not_moving_3_spaces(board1):
    bn11 = piece_at(1, 1, board1)
    bn24 = piece_at(2, 4, board1)
    wn12 = piece_at(1, 2, board1)
    wn52 = piece_at(5, 2, board1)
    wn54 = piece_at(5, 4, board1)

    assert bn11.can_reach(1, 2, board1) is False
    assert bn11.can_reach(5, 1, board1) is False
    assert bn24.can_reach(2, 2, board1) is False
    assert bn24.can_reach(3, 4, board1) is False
    assert bn24.can_reach(1, 1, board1) is False
    assert wn12.can_reach(2, 3, board1) is False
    assert wn52.can_reach(5, 1, board1) is False
    assert wn54.can_reach(2, 3, board1) is False
    # Remaining on the same spot.
    assert wn12.can_reach(1, 2, board1) is False
    assert bn11.can_reach(1, 1, board1) is False


def test_can_reach_knight_moving_3_spaces_in_only_one_dimension(board1):
    '''The knight moves 3 total spaces, but all in a straight line.'''
    bn11 = piece_at(1, 1, board1)
    bn24 = piece_at(2, 4, board1)
    wn12 = piece_at(1, 2, board1)
    wn52 = piece_at(5, 2, board1)

    assert bn11.can_reach(1, 4, board1) is False
    assert bn24.can_reach(5, 4, board1) is False
    assert wn12.can_reach(1, 5, board1) is False
    assert wn52.can_reach(2, 2, board1) is False


def test_can_reach_white_knight_with_valid_movement_landing_on_white_piece(board1, board2):
    wn52 = piece_at(5, 2, board2)
    wn54 = piece_at(5, 4, board1)

    # Landing on white knight.
    assert wn52.can_reach(4, 4, board2) is False
    # Landing on white king.
    assert wn54.can_reach(3, 5, board1) is False


def test_can_reach_black_knight_with_valid_movement_landing_on_black_piece(board1, board2):
    bn11 = piece_at(1, 1, board2)

    # Landing on black knight.
    assert bn11.can_reach(3, 2, board2) is False
    # Landing on black king.
    assert bn11.can_reach(2, 3, board1) is False


def test_can_reach_knight_out_of_bounds_with_valid_movement(board1):
    wn12 = piece_at(1, 2, board1)
    wn52 = piece_at(5, 2, board1)
    bn11 = piece_at(1, 1, board1)
    bn24 = piece_at(2, 4, board1)

    assert wn12.can_reach(-1, 1, board1) is False
    assert wn52.can_reach(7, 3, board1) is False
    assert bn11.can_reach(3, 0, board1) is False
    assert bn24.can_reach(3, 6, board1) is False


def test_can_reach_king_valid_movement_and_no_same_side_piece(board1):
    wk35 = piece_at(3, 5, board1)
    bk23 = piece_at(2, 3, board1)

    # Landing on empty space.
    assert wk35.can_reach(2, 5, board1) is True
    assert wk35.can_reach(3, 4, board1) is True
    assert bk23.can_reach(1, 3, board1) is True
    assert bk23.can_reach(2, 2, board1) is True
    # Landing on opponent knight.
    assert wk35.can_reach(2, 4, board1) is True
    assert bk23.can_reach(1, 2, board1) is True


def test_can_reach_king_moving_more_than_1_space_in_a_single_dimension(board1):
    wk35 = piece_at(3, 5, board1)
    bk23 = piece_at(2, 3, board1)

    assert wk35.can_reach(1, 5, board1) is False
    assert wk35.can_reach(5, 5, board1) is False
    assert wk35.can_reach(3, 2, board1) is False
    assert wk35.can_reach(1, 3, board1) is False
    assert wk35.can_reach(2, 3, board1) is False
    assert bk23.can_reach(2, 1, board1) is False
    assert bk23.can_reach(2, 5, board1) is False
    assert bk23.can_reach(5, 3, board1) is False
    assert bk23.can_reach(4, 1, board1) is False
    assert bk23.can_reach(4, 2, board1) is False


def test_can_reach_king_remaining_on_the_same_spot(board1):
    wk35 = piece_at(3, 5, board1)
    bk23 = piece_at(2, 3, board1)

    assert wk35.can_reach(3, 5, board1) is False
    assert bk23.can_reach(2, 3, board1) is False


def test_can_reach_white_king_with_valid_movement_landing_on_white_piece(board2):
    wk35 = piece_at(3, 5, board2)

    assert wk35.can_reach(4, 4, board2) is False
    assert wk35.can_reach(2, 5, board2) is False


def test_can_reach_black_king_with_valid_movement_landing_on_black_piece(board1, board2):
    bk23 = piece_at(2, 3, board2)

    assert bk23.can_reach(2, 4, board1) is False
    assert bk23.can_reach(3, 2, board2) is False


def test_can_reach_king_out_of_bounds_with_valid_movement(board1):
    wk35 = piece_at(3, 5, board1)

    assert wk35.can_reach(3, 6, board1) is False
    assert wk35.can_reach(2, 6, board1) is False
    assert wk35.can_reach(4, 6, board1) is False


def test_can_move_to_knight_can_move_to_empty_space_and_not_checked(board1):
    wn12 = piece_at(1, 2, board1)
    bn11 = piece_at(1, 1, board1)

    assert wn12.can_move_to(3, 3, board1) is True
    assert bn11.can_move_to(3, 2, board1) is True


def test_can_move_to_knight_can_move_by_capturing_knight_and_not_checked(board1):
    wn12 = piece_at(1, 2, board1)
    bn24 = piece_at(2, 4, board1)

    assert wn12.can_move_to(2, 4, board1) is True
    assert bn24.can_move_to(1, 2, board1) is True


def test_can_move_to_knight_can_move_by_capturing_king_and_checked(board2):
    wn44 = piece_at(4, 4, board2)
    bn43 = piece_at(4, 3, board2)
    
    assert wn44.can_move_to(2, 3, board2) is True
    assert bn43.can_move_to(3, 5, board2) is True


def test_can_move_to_knight_cannot_reach_but_not_checked(board1):
    wn12 = piece_at(1, 2, board1)
    wn52 = piece_at(5, 2, board1)
    wn54 = piece_at(5, 4, board1)
    bn11 = piece_at(1, 1, board1)
    bn24 = piece_at(2, 4, board1)

    # Same side piece.
    assert wn54.can_move_to(3, 5, board1) is False
    assert bn11.can_move_to(2, 3, board1) is False
    # Total squares.
    assert wn12.can_move_to(2, 3, board1) is False
    assert bn24.can_move_to(1, 1, board1) is False
    # Same spot.
    assert wn12.can_move_to(1, 2, board1) is False
    assert bn11.can_move_to(1, 1, board1) is False
    # 3 squares straight.
    assert wn52.can_move_to(2, 2, board1) is False
    assert bn11.can_move_to(1, 4, board1) is False
    # Out of bounds.
    assert wn52.can_move_to(7, 3, board1) is False
    assert bn11.can_move_to(3, 0, board1) is False


def test_can_move_to_knight_can_reach_but_checked(board2):
    wn54 = piece_at(5, 4, board2)
    bn32 = piece_at(3, 2, board2)

    assert wn54.can_move_to(4, 2, board2) is False
    assert bn32.can_move_to(5, 1, board2) is False


def test_can_move_to_knight_can_move_by_removing_check(board2):
    wn51 = Knight(5, 1, True)
    board2[1].append(wn51)
    '''
     ♘♔  
     ♞ ♘♘
     ♚ ♞ 
    ♘ ♞ ♘
    ♞   ♘
    '''
    bn32 = piece_at(3, 2, board2)

    assert wn51.can_move_to(4, 3, board2) is True
    assert bn32.can_move_to(4, 4, board2) is True


def test_can_move_to_knight_board_not_mutated(board2):
    wn51 = Knight(5, 1, True)
    board2[1].append(wn51)
    '''
     ♘♔  
     ♞ ♘♘
     ♚ ♞ 
    ♘ ♞ ♘
    ♞   ♘
    '''
    bn32 = piece_at(3, 2, board2)

    wn51.can_move_to(4, 3, board2)
    bn32.can_move_to(4, 4, board2)

    assert len(board2[1]) == 12


def test_can_move_to1():
    assert wk1.can_move_to(4,5, B1) == False


def test_can_move_to_king_can_move_to_empty_space_and_not_checked(board1):
    wk35 = piece_at(3, 5, board1)
    bk23 = piece_at(2, 3, board1)

    assert wk35.can_move_to(2, 5, board1) is True
    assert bk23.can_move_to(1, 4, board1) is True


def test_can_move_to_king_can_move_by_capturing_knight_and_not_checked(board1):
    bn25 = Knight(2, 5, False)
    board1[1].append(bn25)
    '''
     ♞♔  
     ♞  ♘
     ♚   
    ♘   ♘
    ♞    
    '''
    wk35 = piece_at(3, 5, board1)
    bk23 = piece_at(2, 3, board1)

    assert wk35.can_move_to(2, 5, board1) is True
    assert bk23.can_move_to(1, 2, board1) is True


def test_can_move_to_king_can_move_by_capturing_king_and_checked(board2):
    wk35 = piece_at(3, 5, board2)
    wk35.pos_y = 3
    '''
     ♘   
     ♞ ♘♘
     ♚♔♞ 
    ♘ ♞ ♘
    ♞    
    '''
    bk23 = piece_at(2, 3, board2)
    
    assert wk35.can_move_to(2, 3, board2) is True
    assert bk23.can_move_to(3, 3, board2) is True


def test_can_move_to_king_cannot_reach_but_not_checked(board1):
    wk35 = piece_at(3, 5, board1)
    bk23 = piece_at(2, 3, board1)

    # Same side piece.
    assert bk23.can_move_to(2, 4, board1) is False
    # Total squares.
    assert wk35.can_move_to(3, 3, board1) is False
    assert bk23.can_move_to(4, 1, board1) is False
    # Same spot.
    assert wk35.can_move_to(3, 5, board1) is False
    assert bk23.can_move_to(2, 3, board1) is False
    # Out of bounds.
    assert wk35.can_move_to(3, 6, board1) is False


def test_can_move_to_king_can_reach_but_checked(board1):
    wk35 = piece_at(3, 5, board1)
    bk23 = piece_at(2, 3, board1)

    # Checked by a king.
    assert wk35.can_move_to(3, 4, board1) is False
    # Checked by a knight.
    assert bk23.can_move_to(3, 3, board1) is False
    
    
def test_can_move_to_king_can_move_out_of_check(board2):
    wn25 = piece_at(2, 5, board2)
    board2[1].remove(wn25)
    '''
      ♔  
     ♞ ♘♘
     ♚ ♞ 
    ♘ ♞ ♘
    ♞    
    '''
    wk35 = piece_at(3, 5, board2)
    bk23 = piece_at(2, 3, board2)

    assert wk35.can_move_to(2, 5, board2) is True
    # With capturing.
    assert bk23.can_move_to(1, 2, board2) is True


def test_can_move_to_king_board_not_mutated(board1):
    bn25 = Knight(2, 5, False)
    board1[1].append(bn25)
    '''
     ♞♔  
     ♞  ♘
     ♚   
    ♘   ♘
    ♞    
    '''
    wk35 = piece_at(3, 5, board1)
    bk23 = piece_at(2, 3, board1)

    wk35.can_move_to(2, 5, board1)
    bk23.can_move_to(1, 2, board1)

    assert len(board1[1]) == 8


def test_move_to1():
    Actual_B = wn1.move_to(2,4, B1)
    wn1a = Knight(2,4,True)
    Expected_B = (5, [wn1a, bn1, wn2, wn3, wk1, bk1]) 
    '''
      ♔  
     ♘  ♘
     ♚   
        ♘
    ♞    
    '''

    #check if actual board has same contents as expected 
    assert Actual_B[0] == 5

    for piece1 in Actual_B[1]: #we check if every piece in Actual_B is also present in Expected_B; if not, the test will fail
        found = False
        for piece in Expected_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found


    for piece in Expected_B[1]:  #we check if every piece in Expected_B is also present in Actual_B; if not, the test will fail
        found = False
        for piece1 in Actual_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found


def test_move_to_white_knight_no_capture(board2):
    wn25 = piece_at(2, 5, board2)

    result_board = wn25.move_to(1, 3, board2)

    wn13 = Knight(1, 3, True)
    board2[1].remove(wn25)
    board2[1].append(wn13)

    assert result_board[0] == board2[0]
    assert len(result_board[1]) == len(board2[1])
    for result_piece in result_board[1]:
        found = False
        for expected_piece in board2[1]:
            if (
                    result_piece.pos_x == expected_piece.pos_x
                    and result_piece.pos_y == expected_piece.pos_y
                    and result_piece.side == expected_piece.side
                    and isinstance(result_piece, Knight) == isinstance(expected_piece, Knight)
                    and result_piece is not expected_piece
            ):
                found = True
        assert found is True


def test_move_to_white_knight_captured_a_king(board2):
    wn44 = piece_at(4, 4, board2)

    result_board = wn44.move_to(2, 3, board2)
    
    bk23 = piece_at(2, 3, board2)
    wn23 = Knight(2, 3, True)
    board2[1].remove(wn44)
    board2[1].remove(bk23)
    board2[1].append(wn23)

    assert result_board[0] == board2[0]
    assert len(result_board[1]) == len(board2[1])
    for result_piece in result_board[1]:
        found = False
        for expected_piece in board2[1]:
            if (
                    result_piece.pos_x == expected_piece.pos_x
                    and result_piece.pos_y == expected_piece.pos_y
                    and result_piece.side == expected_piece.side
                    and isinstance(result_piece, Knight) == isinstance(expected_piece, Knight)
                    and result_piece is not expected_piece
            ):
                found = True
        assert found is True


def test_move_to_black_knight_captured_a_knight(board2):
    bn32 = piece_at(3, 2, board2)

    result_board = bn32.move_to(4, 4, board2)

    wn44 = piece_at(4, 4, board2)
    bn44 = Knight(4, 4, False)
    board2[1].remove(bn32)
    board2[1].remove(wn44)
    board2[1].append(bn44)

    assert result_board[0] == board2[0]
    assert len(result_board[1]) == len(board2[1])
    for result_piece in result_board[1]:
        found = False
        for expected_piece in board2[1]:
            if (
                    result_piece.pos_x == expected_piece.pos_x
                    and result_piece.pos_y == expected_piece.pos_y
                    and result_piece.side == expected_piece.side
                    and isinstance(result_piece, Knight) == isinstance(expected_piece, Knight)
                    and result_piece is not expected_piece
            ):
                found = True
        assert found is True


def test_move_to_black_knight_no_capture(board2):
    bn32 = piece_at(3, 2, board2)

    result_board = bn32.move_to(5, 1, board2)
    
    bn51 = Knight(5, 1, False)
    board2[1].remove(bn32)
    board2[1].append(bn51)

    assert result_board[0] == board2[0]
    assert len(result_board[1]) == len(board2[1])
    for result_piece in result_board[1]:
        found = False
        for expected_piece in board2[1]:
            if (
                    result_piece.pos_x == expected_piece.pos_x
                    and result_piece.pos_y == expected_piece.pos_y
                    and result_piece.side == expected_piece.side
                    and isinstance(result_piece, Knight) == isinstance(expected_piece, Knight)
                    and result_piece is not expected_piece
            ):
                found = True
        assert found is True


def test_move_to_black_knight_captured_a_king(board2):
    bn43 = piece_at(4, 3, board2)

    result_board = bn43.move_to(3, 5, board2)

    wk35 = piece_at(3, 5, board2)
    bn35 = Knight(3, 5, False)
    board2[1].remove(bn43)
    board2[1].remove(wk35)
    board2[1].append(bn35)

    assert result_board[0] == board2[0]
    assert len(result_board[1]) == len(board2[1])
    for result_piece in result_board[1]:
        found = False
        for expected_piece in board2[1]:
            if (
                    result_piece.pos_x == expected_piece.pos_x
                    and result_piece.pos_y == expected_piece.pos_y
                    and result_piece.side == expected_piece.side
                    and isinstance(result_piece, Knight) == isinstance(expected_piece, Knight)
                    and result_piece is not expected_piece
            ):
                found = True
        assert found is True


def test_move_to_knight_returned_board_is_the_same_identity(board2):
    bn32 = piece_at(3, 2, board2)

    result_board = bn32.move_to(4, 4, board2)

    assert len(board2[1]) == 11
    assert isinstance(result_board, tuple)
    assert result_board is not board2


@pytest.fixture(scope="function")
def board4():
    '''
     ♞   
     ♞♔ ♘
     ♚   
    ♘   ♘
    ♞    
    '''
    wn12 = Knight(1, 2, True)
    wn52 = Knight(5, 2, True)
    wn54 = Knight(5, 4, True)
    wk34 = King(3, 4, True)
    bn11 = Knight(1, 1, False)
    bn24 = Knight(2, 4, False)
    bn25 = Knight(2, 5, False)
    bk23 = King(2, 3, False)

    return (5, [wn12, wn52, wn54, wk34, bn11, bn24, bn25, bk23])


def test_move_to_white_king_captured_a_knight(board4):
    wk34 = piece_at(3, 4, board4)

    result_board = wk34.move_to(2, 5, board4)

    bn25 = piece_at(2, 5, board4)
    wk25 = King(2, 5, True)
    board4[1].remove(wk34)
    board4[1].remove(bn25)
    board4[1].append(wk25)

    assert result_board[0] == board4[0]
    assert len(result_board[1]) == len(board4[1])
    for result_piece in result_board[1]:
        found = False
        for expected_piece in board4[1]:
            if (
                    result_piece.pos_x == expected_piece.pos_x
                    and result_piece.pos_y == expected_piece.pos_y
                    and result_piece.side == expected_piece.side
                    and isinstance(result_piece, King) == isinstance(expected_piece, King)
                    and result_piece is not expected_piece
            ):
                found = True
        assert found is True
    

def test_move_to_white_king_no_capture(board4):
    wk34 = piece_at(3, 4, board4)

    result_board = wk34.move_to(4, 5, board4)

    wk45 = King(4, 5, True)
    board4[1].remove(wk34)
    board4[1].append(wk45)

    assert result_board[0] == board4[0]
    assert len(result_board[1]) == len(board4[1])
    for result_piece in result_board[1]:
        found = False
        for expected_piece in board4[1]:
            if (
                    result_piece.pos_x == expected_piece.pos_x
                    and result_piece.pos_y == expected_piece.pos_y
                    and result_piece.side == expected_piece.side
                    and isinstance(result_piece, King) == isinstance(expected_piece, King)
                    and result_piece is not expected_piece
            ):
                found = True
        assert found is True


def test_move_to_black_king_captured_a_knight(board4):
    bk23 = piece_at(2, 3, board4)

    result_board = bk23.move_to(1, 2, board4)

    wn12 = piece_at(1, 2, board4)
    bk12 = King(1, 2, False)
    board4[1].remove(bk23)
    board4[1].remove(wn12)
    board4[1].append(bk12)

    assert result_board[0] == board4[0]
    assert len(result_board[1]) == len(board4[1])
    for result_piece in result_board[1]:
        found = False
        for expected_piece in board4[1]:
            if (
                    result_piece.pos_x == expected_piece.pos_x
                    and result_piece.pos_y == expected_piece.pos_y
                    and result_piece.side == expected_piece.side
                    and isinstance(result_piece, King) == isinstance(expected_piece, King)
                    and result_piece is not expected_piece
            ):
                found = True
        assert found is True


def test_move_to_black_king_no_capture(board4):
    bk23 = piece_at(2, 3, board4)

    result_board = bk23.move_to(1, 3, board4)

    bk13 = King(1, 3, False)
    board4[1].remove(bk23)
    board4[1].append(bk13)

    assert result_board[0] == board4[0]
    assert len(result_board[1]) == len(board4[1])
    for result_piece in result_board[1]:
        found = False
        for expected_piece in board4[1]:
            if (
                    result_piece.pos_x == expected_piece.pos_x
                    and result_piece.pos_y == expected_piece.pos_y
                    and result_piece.side == expected_piece.side
                    and isinstance(result_piece, King) == isinstance(expected_piece, King)
                    and result_piece is not expected_piece
            ):
                found = True
        assert found is True


def test_move_to_king_returned_board_is_the_same_identity(board4):
    wk34 = piece_at(3, 4, board4)

    result_board = wk34.move_to(2, 5, board4)

    assert len(board4[1]) == 8
    assert isinstance(result_board, tuple)
    assert result_board is not board4


def test_is_check1():
    wk1a = King(4,5,True)
    B2 = (5, [wn1, bn1, wn2, bn2, wn3, wk1a, bk1])
    '''
       ♔ 
     ♞  ♘
     ♚   
    ♘   ♘
    ♞    
    '''
    
    assert is_check(True, B2) == True


@pytest.fixture(scope="function")
def board3():
    '''
     ♘   
     ♞♔ ♘
     ♚ ♞ 
    ♘ ♞ ♘
    ♞    
    '''
    wn12 = Knight(1, 2, True)
    wn52 = Knight(5, 2, True)
    wn54 = Knight(5, 4, True)
    wn25 = Knight(2, 5, True)
    wk35 = King(3, 4, True)

    bn11 = Knight(1, 1, False)
    bn24 = Knight(2, 4, False)
    bn32 = Knight(3, 2, False)
    bn43 = Knight(4, 3, False)
    bk23 = King(2, 3, False)

    return (5, [wn12, bn11, wn52, bn24, wn54, wk35, bk23, wn25, bn32, bn43])
    
def test_is_check_white_king_checked_by_black_king(board3):
    assert is_check(True, board3) is True


def test_is_check_black_king_checked_by_white_knight(board2):
    assert is_check(False, board2) is True


def test_is_check_black_king_checked_by_white_king(board3):
    assert is_check(False, board3) is True


def test_is_check_king_not_in_check():
    assert is_check(True, B1) is False
    assert is_check(False, B1) is False


def test_is_checkmate1():
    wk1a = King(1,5,True)
    bn2a = Knight(3,4, False)
    bn3 = Knight(4,4,False)
    B2 = (5, [wn1, wn2, wn3, wk1a, bn1, bk1, bn2a, bn3])
  
    '''
    ♔    
      ♞♞♘
     ♚   
    ♘   ♘
    ♞    
    '''
    assert is_checkmate(True, B2) == True


def test_is_checkmate_false_with_king_checking():
    '''
        
        
     ♔  
    ♚   
    '''
    wk22 = King(2, 2, True)
    bk11 = King(1, 1, False)
    board = (4, [wk22, bk11])

    assert is_checkmate(False, board) is False

    # Swap the sides.
    bk22 = King(2, 2, False)
    wk11 = King(1, 1, True)
    board = (4, [bk22, wk11])

    assert is_checkmate(True, board) is False


def test_is_checkmate_false_with_king_checking_and_zoning_and_blocking():
    '''
     ♘  
        
     ♔  
    ♚♞  
    '''
    wk22 = King(2, 2, True)
    wn24 = Knight(2, 4, True)
    bk11 = King(1, 1, False)
    bn21 = Knight(2, 1, False)
    board = (4, [wk22, wn24, bk11, bn21])

    assert is_checkmate(False, board) is False

    # Swap the sides.
    bk22 = King(2, 2, False)
    bn24 = Knight(2, 4, False)
    wk11 = King(1, 1, True)
    wn21 = Knight(2, 1, True)
    board = (4, [bk22, bn24, wk11, wn21])

    assert is_checkmate(True, board) is False


def test_is_checkmate_false_with_knight_checking_and_escape_zones():
    '''
        
     ♘  
        
    ♚ ♔ 
    '''
    wk31 = King(3, 1, True)
    wn23 = Knight(2, 3, True)
    bk11 = King(1, 1, False)
    board = (4, [wk31, wn23, bk11])

    assert is_checkmate(False, board) is False

    # Swap the sides.
    bk31 = King(3, 1, False)
    bn23 = Knight(2, 3, False)
    wk11 = King(1, 1, True)
    board = (4, [bk31, bn23, wk11])

    assert is_checkmate(True, board) is False

    
def test_is_checkmate_true_with_knight_checking_and_zoning_and_blocking():
    '''
     ♘  
     ♘  
      ♔ 
    ♚♞  
    '''
    wk32 = King(3, 2, True)
    wn23 = Knight(2, 3, True)
    wn24 = Knight(2, 4, True)
    bk11 = King(1, 1, False)
    bn21 = Knight(2, 1, False)
    board = (4, [wk32, wn23, wn24, bk11, bn21])

    assert is_checkmate(False, board) is True

    # Swap the sides.
    bk32 = King(3, 2, False)
    bn23 = Knight(2, 3, False)
    bn24 = Knight(2, 4, False)
    wk11 = King(1, 1, True)
    wn21 = Knight(2, 1, True)
    board = (4, [bk32, bn23, bn24, wk11, wn21])

    assert is_checkmate(True, board) is True


def test_is_checkmate_true_with_knight_checking_and_zoning_and_blocking_and_getting_checked():
    '''Technically impossible scenario.'''
    '''
         
     ♘   
     ♘  ♞
      ♔  
    ♚♞   
    '''
    wk32 = King(3, 2, True)
    wn23 = Knight(2, 3, True)
    wn24 = Knight(2, 4, True)
    bk11 = King(1, 1, False)
    bn21 = Knight(2, 1, False)
    bn53 = Knight(5, 3, False)
    board = (4, [wk32, wn23, wn24, bk11, bn21, bn53])

    assert is_checkmate(False, board) is True

    # Swap the sides.
    bk32 = King(3, 2, False)
    bn23 = Knight(2, 3, False)
    bn24 = Knight(2, 4, False)
    wk11 = King(1, 1, True)
    wn21 = Knight(2, 1, True)
    wn53 = Knight(5, 3, True)
    board = (4, [bk32, bn23, bn24, wk11, wn21, wn53])

    assert is_checkmate(True, board) is True


def test_is_checkmate_false_with_no_check():
    '''
     ♘  
     ♞  
      ♔ 
    ♚♞  
    '''
    wk32 = King(3, 2, True)
    wn24 = Knight(2, 4, True)
    bk11 = King(1, 1, False)
    bn21 = Knight(2, 1, False)
    bn23 = Knight(2, 3, False)
    board = (4, [wk32, wn24, bk11, bn21, bn23])

    assert is_checkmate(False, board) is False

    # Swap the sides.
    bk32 = King(3, 2, False)
    bn24 = Knight(2, 4, False)
    wk11 = King(1, 1, True)
    wn21 = Knight(2, 1, True)
    wn23 = Knight(2, 3, True)
    board = (4, [bk32, bn24, wk11, wn21, wn23])

    assert is_checkmate(True, board) is False


def test_is_checkmate_false_with_knight_that_can_be_eaten_and_zoning_and_blocking():
    '''
       ♞ 
     ♘   
     ♘   
      ♔  
    ♚♞   
    '''
    wk32 = King(3, 2, True)
    wn23 = Knight(2, 3, True)
    wn24 = Knight(2, 4, True)
    bk11 = King(1, 1, False)
    bn21 = Knight(2, 1, False)
    bn35 = Knight(3, 5, False)
    board = (5, [wk32, wn23, wn24, bk11, bn21, bn35])

    assert is_checkmate(False, board) is False

    # Swap the sides.
    bk32 = King(3, 2, False)
    bn23 = Knight(2, 3, False)
    bn24 = Knight(2, 4, False)
    wk11 = King(1, 1, True)
    wn21 = Knight(2, 1, True)
    wn35 = Knight(3, 5, True)
    board = (4, [bk32, bn23, bn24, wk11, wn21, wn35])

    assert is_checkmate(True, board) is False


def test_is_checkmate_true_with_knight_that_cant_be_eaten_by_same_side_and_zoning_and_blocking():
    '''
      ♘  
     ♘   
     ♘   
      ♔  
    ♚♞   
    '''
    wk32 = King(3, 2, True)
    wn23 = Knight(2, 3, True)
    wn24 = Knight(2, 4, True)
    wn35 = Knight(3, 5, True)
    bk11 = King(1, 1, False)
    bn21 = Knight(2, 1, False)
    board = (5, [wk32, wn23, wn24, wn35, bk11, bn21])

    assert is_checkmate(False, board) is True

    # Swap the sides.
    bk32 = King(3, 2, False)
    bn23 = Knight(2, 3, False)
    bn24 = Knight(2, 4, False)
    bn35 = Knight(3, 5, False)
    wk11 = King(1, 1, True)
    wn21 = Knight(2, 1, True)
    board = (4, [bk32, bn23, bn24, bn35, wk11, wn21])

    assert is_checkmate(True, board) is True


def test_is_checkmate_false_with_blocker_that_can_be_eaten_and_zoning():
    '''
     ♘♘  
      ♘♔ 
         
    ♞♚♘  
    ♞♞♞  
    '''
    wk44 = King(4, 4, True)
    wn32 = Knight(3, 2, True)
    wn34 = Knight(3, 4, True)
    wn25 = Knight(2, 5, True)
    wn35 = Knight(3, 5, True)
    bk22 = King(2, 2, False)
    bn11 = Knight(1, 1, False)
    bn21 = Knight(2, 1, False)
    bn31 = Knight(3, 1, False)
    bn12 = Knight(1, 2, False)
    board = (5, [wk44, wn32, wn34, wn25, wn35, bk22, bn11, bn21, bn31, bn12])

    assert is_checkmate(False, board) is False

    # Swap the sides.
    bk44 = King(4, 4, False)
    bn32 = Knight(3, 2, False)
    bn34 = Knight(3, 4, False)
    bn25 = Knight(2, 5, False)
    bn35 = Knight(3, 5, False)
    wk22 = King(2, 2, True)
    wn11 = Knight(1, 1, True)
    wn21 = Knight(2, 1, True)
    wn31 = Knight(3, 1, True)
    wn12 = Knight(1, 2, True)
    board = (5, [bk44, bn32, bn34, bn25, bn35, wk22, wn11, wn21, wn31, wn12])

    assert is_checkmate(True, board) is False


def test_is_stalemate_another_same_side_piece_remaining():
    '''
     ♘ ♞
        
        
    ♚ ♔ 
    '''
    wk31 = King(3, 1, True)
    wn24 = Knight(2, 4, True)
    bk11 = King(1, 1, False)
    bn44 = Knight(4, 4, False)
    board = (4, [wk31, wn24, bk11, bn44])

    assert is_stalemate(False, board) is False

    # Swap the sides.
    bk31 = King(3, 1, False)
    bn24 = Knight(2, 4, False)
    wk11 = King(1, 1, True)
    wn44 = Knight(4, 4, True)
    board = (4, [bk31, bn24, wk11, wn44])

    assert is_stalemate(True, board) is False


def test_is_stalemate_getting_checkmated():
    '''
     ♘  
     ♘  
        
    ♚ ♔ 
    '''
    wk31 = King(3, 1, True)
    wn24 = Knight(2, 4, True)
    wn23 = Knight(2, 3, True)
    bk11 = King(1, 1, False)
    board = (4, [wk31, wn24, wn23, bk11])

    assert is_stalemate(False, board) is False
    
    # Swap the sides.
    bk31 = King(3, 1, False)
    bn24 = Knight(2, 4, False)
    bn23 = Knight(2, 3, False)
    wk11 = King(1, 1, True)
    board = (4, [bk31, bn24, bn23, wk11])

    assert is_stalemate(True, board) is False


def test_is_stalemate_getting_checked():
    '''
        
     ♘  
        
    ♚ ♔ 
    '''
    wk31 = King(3, 1, True)
    wn23 = Knight(2, 3, True)
    bk11 = King(1, 1, False)
    board = (4, [wk31, wn23, bk11])

    assert is_stalemate(False, board) is False
    
    # Swap the sides.
    bk31 = King(3, 1, False)
    bn23 = Knight(2, 3, False)
    wk11 = King(1, 1, True)
    board = (4, [bk31, bn23, wk11])

    assert is_stalemate(True, board) is False


def test_is_stalemate_has_empty_escape_zones():
    '''
       
       
    ♚ ♔
    '''
    wk31 = King(3, 1, True)
    bk11 = King(1, 1, False)
    board = (3, [wk31, bk11])

    assert is_stalemate(False, board) is False
    
    bk31 = King(3, 1, False)
    wk11 = King(1, 1, True)
    board = (3, [bk31, wk11])

    assert is_stalemate(True, board) is False


def test_is_stalemate_can_escape_by_eating_blockers():
    '''
        
        
    ♘   
    ♚ ♔ 
    '''
    wk31 = King(3, 1, True)
    wn12 = Knight(1, 2, True)
    bk11 = King(1, 1, False)
    board = (4, [wk31, wn12, bk11])

    assert is_stalemate(False, board) is False

    bk31 = King(3, 1, False)
    bn12 = Knight(1, 2, False)
    wk11 = King(1, 1, True)
    board = (4, [bk31, bn12, wk11])

    assert is_stalemate(True, board) is False


def test_is_stalemate_true_with_zoning():
    '''
     ♘  
        
        
    ♚ ♔ 
    '''
    wk31 = King(3, 1, True)
    wn24 = Knight(2, 4, True)
    bk11 = King(1, 1, False)
    board = (4, [wk31, wn24, bk11])

    assert is_stalemate(False, board) is True
    
    bk31 = King(3, 1, False)
    bn24 = Knight(2, 4, False)
    wk11 = King(1, 1, True)
    board = (4, [bk31, bn24, wk11])

    assert is_stalemate(True, board) is True


def test_read_board1():
    B = read_board("board_examp.txt")
    for piece in B[1]:
        print(f'{piece.pos_x}, {piece.pos_y}, {piece.side}, {type(piece)}')
    print()
    for piece in B1[1]:
        print(f'{piece.pos_x}, {piece.pos_y}, {piece.side}, {type(piece)}')
    assert B[0] == 5

    for piece in B[1]:  #we check if every piece in B is also present in B1; if not, the test will fail
        found = False
        for piece1 in B1[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

    for piece1 in B1[1]: #we check if every piece in B1 is also present in B; if not, the test will fail
        found = False
        for piece in B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found


def test_read_board_file_doesnt_exist():
    with pytest.raises(FileNotFoundError) as e:
        read_board('data/test_read_board_file_doesnt_exist.txt')
    assert str(e.value) == 'File does not exist.'


def test_read_board_less_than_3_lines():
    with pytest.raises(IOError) as e:
        read_board('data/test_read_board_less_than_3_lines.txt')
    assert str(e.value) == 'There are less than 3 lines in the file.'


def test_read_board_first_line_not_an_int():
    with pytest.raises(IOError) as e:
        read_board('data/test_read_board_first_line_not_an_int.txt')
    assert str(e.value) == 'Board size is not an integer.'


def test_read_board_board_size_out_of_range():
    with pytest.raises(IOError) as e:
        read_board('data/test_read_board_board_size_out_of_range_1.txt')
    assert str(e.value) == 'Board size is not within 3 to 26.'
    with pytest.raises(IOError) as e:
        read_board('data/test_read_board_board_size_out_of_range_2.txt')
    assert str(e.value) == 'Board size is not within 3 to 26.'


def test_read_board_empty_letter_for_piece_type():
    with pytest.raises(IOError) as e:
        read_board('data/test_read_board_empty_letter_for_piece_type.txt')
    assert str(e.value) == 'Piece type is empty.'


def test_read_board_letters_other_than_N_or_K():
    with pytest.raises(IOError) as e:
        read_board('data/test_read_board_letters_other_than_N_or_K.txt')
    assert str(e.value) == 'Piece type other than N or K was found.'


def test_read_board_no_commas():
    with pytest.raises(IOError) as e:
        read_board('data/test_read_board_no_commas.txt')
    assert str(e.value) == 'Piece type is empty.'


def test_read_board_more_than_1_king():
    with pytest.raises(IOError) as e:
        read_board('data/test_read_board_more_than_1_king.txt')
    assert str(e.value) == 'At least one side contains more than 1 king.'


def test_read_board_location2index_returns_invalid():
    with pytest.raises(IOError) as e:
        read_board('data/test_read_board_location2index_returns_empty_string.txt')
    assert str(e.value) == 'Location is empty.'
    with pytest.raises(IOError) as e:
        read_board('data/test_read_board_location2index_returns_invalid_column_integer.txt')
    assert str(e.value) == 'Column is out of the range of characters a to z.'
    with pytest.raises(IOError) as e:
        read_board('data/test_read_board_location2index_returns_invalid_column_caps.txt')
    assert str(e.value) == 'Column is out of the range of characters a to z.'
    with pytest.raises(IOError) as e:
        read_board('data/test_read_board_location2index_returns_invalid_column_non_letter.txt')
    assert str(e.value) == 'Column is out of the range of characters a to z.'
    with pytest.raises(IOError) as e:
        read_board('data/test_read_board_location2index_returns_invalid_row_empty.txt')
    assert str(e.value) == 'Row is incorrectly formatted.'
    with pytest.raises(IOError) as e:
        read_board('data/test_read_board_location2index_returns_invalid_row_non_integer_1.txt')
    assert str(e.value) == 'Row is incorrectly formatted.'
    with pytest.raises(IOError) as e:
        read_board('data/test_read_board_location2index_returns_invalid_row_non_integer_2.txt')
    assert str(e.value) == 'Row is incorrectly formatted.'


def test_read_board_column_out_of_range():
    with pytest.raises(IOError) as e:
        read_board('data/test_read_board_column_out_of_range.txt')
    assert str(e.value) == 'Column is not within 1 to max board size.'


def test_read_board_row_out_of_range():
    with pytest.raises(IOError) as e:
        read_board('data/test_read_board_row_out_of_range.txt')
    assert str(e.value) == 'Row is not within 1 to max board size.'


def test_read_board_arbitrary_spaces(board1):
    result_board = read_board('data/test_read_board_arbitrary_spaces.txt')
    
    assert result_board[0] == 5
    assert len(result_board[1]) == len(board1[1])

    for result_piece in result_board[1]:
        found = False
        for expected_piece in board1[1]:
            if (
                    result_piece.pos_x == expected_piece.pos_x
                    and result_piece.pos_y == expected_piece.pos_y
                    and result_piece.side == expected_piece.side
                    and type(result_piece) == type(expected_piece)
            ):
                found = True
        assert found is True


def test_read_board_pieces_in_same_location():
    with pytest.raises(IOError) as e:
        read_board('data/test_read_board_pieces_in_same_location.txt')
    assert str(e.value) == 'There are pieces in the same location.'


def test_conf2unicode_1(board1):
    expected = '\u2001\u2001\u2654\u2001\u2001' + '\n'
    expected += '\u2001\u265E\u2001\u2001\u2658' + '\n'
    expected += '\u2001\u265A\u2001\u2001\u2001' + '\n'
    expected += '\u2658\u2001\u2001\u2001\u2658' + '\n'
    expected += '\u265E\u2001\u2001\u2001\u2001' + '\n'

    assert conf2unicode(board1) == expected


def test_conf2unicode_2(board2):
    expected = '\u2001\u2658\u2654\u2001\u2001' + '\n'
    expected += '\u2001\u265E\u2001\u2658\u2658' + '\n'
    expected += '\u2001\u265A\u2001\u265E\u2001' + '\n'
    expected += '\u2658\u2001\u265E\u2001\u2658' + '\n'
    expected += '\u265E\u2001\u2001\u2001\u2001' + '\n'

    assert conf2unicode(board2) == expected


def test_conf2unicode_3(board3):
    expected = '\u2001\u2658\u2001\u2001\u2001' + '\n'
    expected += '\u2001\u265E\u2654\u2001\u2658' + '\n'
    expected += '\u2001\u265A\u2001\u265E\u2001' + '\n'
    expected += '\u2658\u2001\u265E\u2001\u2658' + '\n'
    expected += '\u265E\u2001\u2001\u2001\u2001' + '\n'

    assert conf2unicode(board3) == expected


def test_conf2unicode_smallest_board():
    '''
    ♘ ♔
       
    ♚ ♞
    '''
    wn13 = Knight(1, 3, True)
    wk33 = King(3, 3, True)
    bn31 = Knight(3, 1, False)
    bk11 = King(1, 1, False)
    board = (3, [wn13, wk33, bn31, bk11])

    expected = '\u2658\u2001\u2654' + '\n'
    expected += '\u2001\u2001\u2001' + '\n'
    expected += '\u265A\u2001\u265E' + '\n'

    assert conf2unicode(board) == expected


def test_conf2unicode_largest_board():
    '''
                             ♔
                  ♘           
    ^ repeated 23 more times ^
    ♚                         
    '''
    wk2626 = King(26, 26, True)
    bk11 = King(1, 1, False)
    board = (26, [wk2626, bk11])
    for i in range(2, 26):
        board[1].append(Knight(15, i, True))

    expected = '\u2001\u2001\u2001\u2001\u2001'
    expected += '\u2001\u2001\u2001\u2001\u2001'
    expected += '\u2001\u2001\u2001\u2001\u2001'
    expected += '\u2001\u2001\u2001\u2001\u2001'
    expected += '\u2001\u2001\u2001\u2001\u2001'
    expected += '\u2654' + '\n'
    for _ in range(24):
        expected += '\u2001\u2001\u2001\u2001\u2001'
        expected += '\u2001\u2001\u2001\u2001\u2001'
        expected += '\u2001\u2001\u2001\u2001\u2658'
        expected += '\u2001\u2001\u2001\u2001\u2001'
        expected += '\u2001\u2001\u2001\u2001\u2001'
        expected += '\u2001' + '\n'
    expected += '\u265A\u2001\u2001\u2001\u2001'
    expected += '\u2001\u2001\u2001\u2001\u2001'
    expected += '\u2001\u2001\u2001\u2001\u2001'
    expected += '\u2001\u2001\u2001\u2001\u2001'
    expected += '\u2001\u2001\u2001\u2001\u2001'
    expected += '\u2001' + '\n'

    assert conf2unicode(board) == expected
