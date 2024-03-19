import pytest
from chess_puzzle import *


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


def test_location2index_column_is_invalid():
    with pytest.raises(ValueError) as e:
        location2index('55')
    assert str(e.value) == 'Column is incorrectly formatted.'
    with pytest.raises(ValueError) as e:
        location2index('526')
    assert str(e.value) == 'Column is incorrectly formatted.'


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


def test_is_piece_at_is_true_for_any_colour_pieces():
    assert is_piece_at(1, 2, B1) is True
    assert is_piece_at(5, 2, B1) is True
    assert is_piece_at(5, 4, B1) is True
    assert is_piece_at(3, 5, B1) is True
    assert is_piece_at(1, 1, B1) is True
    assert is_piece_at(2, 3, B1) is True
    assert is_piece_at(2, 4, B1) is True


def test_is_piece_at_one_coordinate_is_out_of_bounds():
    with pytest.raises(ValueError) as e:
        is_piece_at(1, 6, B1)
    assert str(e.value) == 'One of the coordinate is out of bounds.'
    with pytest.raises(ValueError) as e:
        is_piece_at(7, 1, B1)
    assert str(e.value) == 'One of the coordinate is out of bounds.'
    with pytest.raises(ValueError) as e:
        is_piece_at(0, 5, B1)
    assert str(e.value) == 'One of the coordinate is out of bounds.'
    with pytest.raises(ValueError) as e:
        is_piece_at(5, -1, B1)
    assert str(e.value) == 'One of the coordinate is out of bounds.'


def test_piece_at1():
    assert piece_at(1,1, B1) == bn1


def test_can_reach1():
    assert bn1.can_reach(2,2, B1) == False


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
    bk23 = King(2, 3, False)
    bn24 = Knight(2, 4, False)

    return (5, [wn12, bn11, wn52, bn24, wn54, wk35, bk23])


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


def test_can_reach_knight_out_of_bounds_with_valid_movement(board1):
    assert wn12.can_reach(-1, 1, board1) is False
    assert wn52.can_reach(7, 3, board1) is False
    assert bn11.can_reach(3, 0, board1) is False
    assert bn24.can_reach(3, 6, board1) is False


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

    bn11 = Knight(1, 1,False)
    bn24 = Knight(2, 4, False)
    bn32 = Knight(3, 2, False)
    bn43 = Knight(4, 3, False)
    bk23 = King(2, 3, False)

    return (5, [wn12, bn11, wn52, bn24, wn54, wk35, bk23, wn44, wn25, bn32, bn43])


def test_can_reach_white_knight_with_valid_movement_landing_on_white_piece(board1, board2):
    wn52 = piece_at(5, 2, board2)

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


def test_can_reach_knight_valid_movement_and_no_same_side_piece(board1, board2):
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


def test_can_reach_king_moving_more_than_1_space_in_a_single_dimension(board1):
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
    assert wk35.can_reach(3, 5, board1) is False
    assert bk23.can_reach(2, 3, board1) is False


def test_can_reach_king_out_of_bounds_with_valid_movement(board1):
    assert wk35.can_reach(3, 6, board1) is False
    assert wk35.can_reach(2, 6, board1) is False
    assert wk35.can_reach(4, 6, board1) is False


def test_can_reach_white_king_with_valid_movement_landing_on_white_piece(board2):
    wk35 = piece_at(3, 5, board2)

    assert wk35.can_reach(4, 4, board2) is False
    assert wk35.can_reach(2, 5, board2) is False


def test_can_reach_black_king_with_valid_movement_landing_on_black_piece(board1, board2):
    bk23 = piece_at(2, 3, board2)

    assert bk23.can_reach(2, 4, board1) is False
    assert bk23.can_reach(3, 2, board2) is False


def test_can_reach_king_valid_movement_and_no_same_side_piece(board1):
    # Landing on empty space.
    assert wk35.can_reach(2, 5, board1) is True
    assert wk35.can_reach(3, 4, board1) is True
    assert bk23.can_reach(1, 3, board1) is True
    assert bk23.can_reach(2, 2, board1) is True
    # Landing on opponent knight.
    assert wk35.can_reach(2, 4, board1) is True
    assert bk23.can_reach(1, 2, board1) is True


def test_can_move_to_knight_cannot_reach_but_not_checked(board1):
    assert wn54.can_move_to(3, 5, board1) is False
    assert bn11.can_move_to(2, 3, board1) is False
    assert wn12.can_move_to(2, 3, board1) is False
    assert bn24.can_move_to(1, 1, board1) is False
    assert wn12.can_move_to(1, 2, board1) is False
    assert bn11.can_move_to(1, 1, board1) is False
    assert wn52.can_move_to(2, 2, board1) is False
    assert bn11.can_move_to(1, 4, board1) is False
    assert wn52.can_move_to(7, 3, board1) is False
    assert bn11.can_move_to(3, 0, board1) is False


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


def test_can_move_to_knight_can_reach_but_checked(board2):
    wn54 = piece_at(5, 4, board2)
    bn32 = piece_at(3, 2, board2)

    assert wn54.can_move_to(4, 2, board2) is False
    assert bn32.can_move_to(5, 1, board2) is False


def test_can_move_to_knight_can_move_by_removing_check(board2):
    wn31 = Knight(3, 1, True)
    bn32 = piece_at(3, 2, board2)
    board2[1].append(wn31)

    assert wn31.can_move_to(4, 3, board2) is True
    assert bn32.can_move_to(4, 4, board2) is True


def test_can_move_to_knight_can_move_with_capturing(board1, board2):
    wn44 = piece_at(4, 4, board2)
    bn43 = piece_at(4, 3, board2)

    # Capturing knight.
    assert wn12.can_move_to(2, 4, board1) is True
    assert bn24.can_move_to(1, 2, board1) is True
    # Capturing king.
    assert wn44.can_move_to(2, 3, board2) is True
    assert bn43.can_move_to(3, 5, board2) is True


def test_can_move_to_knight_can_move_to_empty_space(board1):
    assert wn12.can_move_to(3, 3, board1) is True
    assert bn11.can_move_to(3, 2, board1) is True


@pytest.mark.skip
def test_can_move_to1():
    assert wk1.can_move_to(4,5, B1) == False


@pytest.mark.skip
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


def test_is_check_white_king_checked_by_black_king(board3):
    assert is_check(True, board3) is True


def test_is_check_black_king_checked_by_white_knight(board2):
    assert is_check(False, board2) is True


def test_is_check_black_king_checked_by_white_king(board3):
    assert is_check(False, board3) is True


def test_is_check_king_not_in_check():
    assert is_check(True, B1) is False
    assert is_check(False, B1) is False


@pytest.mark.skip
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


@pytest.mark.skip
def test_read_board1():
    B = read_board("board_examp.txt")
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
