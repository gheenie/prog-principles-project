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
    assert is_piece_at(1, 2, B1) == True
    assert is_piece_at(5, 2, B1) == True
    assert is_piece_at(5, 4, B1) == True
    assert is_piece_at(3, 5, B1) == True
    assert is_piece_at(1, 1, B1) == True
    assert is_piece_at(2, 3, B1) == True
    assert is_piece_at(2, 4, B1) == True


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
    '''Knight not moving 3 spaces total.'''

    assert bn1.can_reach(2,2, B1) == False
    assert bn1.can_reach(1, 2, B1) == False
    assert bn1.can_reach(5, 1, B1) == False
    assert bn2.can_reach(2, 2, B1) == False
    assert bn2.can_reach(3, 4, B1) == False
    assert bn2.can_reach(1, 1, B1) == False
    assert wn1.can_reach(2, 3, B1) == False
    assert wn2.can_reach(5, 1, B1) == False
    assert wn3.can_reach(2, 3, B1) == False
    # Remaining on the same spot.
    assert wn1.can_reach(1, 2, B1) == False
    assert bn1.can_reach(1, 1, B1) == False


def test_can_reach_knight_moving_3_spaces_in_only_one_dimension():
    '''A knight moves 3 total spaces, but all in a straight line.'''

    assert bn1.can_reach(1, 4, B1) == False
    assert bn2.can_reach(5, 4, B1) == False
    assert wn1.can_reach(1, 5, B1) == False
    assert wn2.can_reach(2, 2, B1) == False


def test_can_reach_king_moving_more_than_1_space_in_a_single_dimension():
    assert wk1.can_reach(1, 5, B1) == False
    assert wk1.can_reach(5, 5, B1) == False
    assert wk1.can_reach(3, 2, B1) == False
    assert wk1.can_reach(1, 3, B1) == False
    assert wk1.can_reach(2, 3, B1) == False
    assert bk1.can_reach(2, 1, B1) == False
    assert bk1.can_reach(2, 5, B1) == False
    assert bk1.can_reach(5, 3, B1) == False
    assert bk1.can_reach(4, 1, B1) == False
    assert bk1.can_reach(4, 2, B1) == False


def test_can_reach_king_remaining_on_the_same_spot():
    assert wk1.can_reach(3, 5, B1) == False
    assert bk1.can_reach(2, 3, B1) == False


def test_can_reach_out_of_bounds_with_valid_movement():
    assert wk1.can_reach(3, 6, B1) == False
    assert wn1.can_reach(-1, 1, B1) == False
    assert wn2.can_reach(7, 3, B1) == False
    assert bn1.can_reach(3, 0, B1) == False
    assert bn2.can_reach(3, 6, B1) == False


def test_can_move_to1():
    assert wk1.can_move_to(4,5, B1) == False


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
