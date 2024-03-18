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


def test_location2index_out_of_bounds():
    pass


def test_index2location1():
    assert index2location(5,2) == "e2"


def test_index2location_row_is_double_digit():
    assert index2location(5, 20) == "e20"
    assert index2location(26, 26) == "z26"


def test_index2location_input_is_not_ints():
    with pytest.raises(TypeError) as e:
        index2location(5, [2])
    assert str(e.value) == 'Indices are not ints.'
    with pytest.raises(TypeError) as e:
        index2location('5', 2)
    assert str(e.value) == 'Indices are not ints.'


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


def test_piece_at1():
    assert piece_at(1,1, B1) == bn1


def test_can_reach1():
    assert bn1.can_reach(2,2, B1) == False


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
