from copy import deepcopy
from copy import copy
from typing import Optional
from collections import namedtuple


def location2index(loc: str) -> tuple[int, int]:
    '''converts chess location to corresponding x and y coordinates'''
    # Check edge cases.
    if isinstance(loc, str) is False:
        raise TypeError('Location is not a string.')
    if loc == '':
        raise ValueError('Location is empty.')
    
    column = loc[0]
    row = loc[1:]
    converted_column = ord(column) - 96

    # Check edge cases.
    if converted_column<1 or converted_column>26:
        raise ValueError('Column is out of the range of characters a to z.')
    try:
        row = int(row)
    except ValueError:
        raise ValueError('Row is incorrectly formatted.')
    if row<1 or row>26:
        raise ValueError('The row is out of bounds.')
    
    return (converted_column, row)


def index2location(x: int, y: int) -> str:
    '''converts  pair of coordinates to corresponding location'''
    # Check edge cases.
    if isinstance(x, int) is False or isinstance(y, int) is False:
        raise TypeError('One of the indices is not an integer.')
    if x<1 or x>26:
        raise ValueError('The column is out of bounds.')
    if y<1 or y>26:
        raise ValueError('The row is out of bounds.')

    return f'{chr(x + 96)}{y}'


class Piece:
    pos_x : int	
    pos_y : int
    side : bool #True for White and False for Black

    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values'''
        self.pos_x = pos_X
        self.pos_y = pos_Y
        self.side = side_


Board = tuple[int, list[Piece]]


def is_piece_at(pos_X : int, pos_Y : int, B: Board) -> bool:
    '''checks if there is piece at coordinates pox_X, pos_Y of board B''' 
    # Check edge cases.
    if pos_X<1 or pos_X>B[0] or pos_Y<1 or pos_Y>B[0]:
        raise ValueError('One of the coordinate is out of bounds.')

    for piece in B[1]:
        if piece.pos_x==pos_X and piece.pos_y==pos_Y:
            return True
        
    return False


def piece_at(pos_X : int, pos_Y : int, B: Board) -> Piece:
    '''
    returns the piece at coordinates pox_X, pos_Y of board B 
    assumes some piece at coordinates pox_X, pos_Y of board B is present
    '''
    for piece in B[1]:
        if piece.pos_x==pos_X and piece.pos_y==pos_Y:
            return piece


def get_piece_or_none(pos_X: int, pos_Y: int, B: Board) -> Optional[Piece]:
    '''
    Returns the piece at the specified coordinates if one is present,
    otherwise return None.
    '''
    piece = None
    if is_piece_at(pos_X, pos_Y, B):
        piece = piece_at(pos_X, pos_Y, B)
        
    return piece


class Knight(Piece):
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X, pos_Y, side_)
	
    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''
        checks if this knight can move to coordinates pos_X, pos_Y
        on board B according to rule [Rule1] and [Rule3] (see section Intro)
        Hint: use is_piece_at
        '''
        # Check rule 1.
        if not (
                abs(self.pos_x-pos_X)==2 and abs(self.pos_y-pos_Y)==1
                or abs(self.pos_x-pos_X)==1 and abs(self.pos_y-pos_Y)==2
        ):
            return False
        
        # Check rule 3.
        try:
            stationary_piece = get_piece_or_none(pos_X, pos_Y, B)
            if stationary_piece is None:
                return True
            return stationary_piece.side is not self.side
        except ValueError as e:
            # Handle edge cases.
            if e.args[0] == 'One of the coordinate is out of bounds.':
                return False
            
    def can_move_to(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''
        checks if this knight can move to coordinates pos_X, pos_Y
        on board B according to all chess rules
        
        Hints:
        - firstly, check [Rule1] and [Rule3] using can_reach
        - secondly, check if result of move is capture using is_piece_at
        - if yes, find the piece captured using piece_at
        - thirdly, construct new board resulting from move
        - finally, to check [Rule4], use is_check on new board
        '''
        board_copy = deepcopy(B)

        if self.can_reach(pos_X, pos_Y, board_copy) is False:
            return False
        
        # Remove any enemy pieces.
        stationary_piece = get_piece_or_none(pos_X, pos_Y, board_copy)
        if stationary_piece is not None:
            # Move is immediately valid if king is eaten.
            if isinstance(stationary_piece, King) is True:
                return True
            board_copy[1].remove(stationary_piece)
        
        # Move the current piece.
        self_copy = piece_at(self.pos_x, self.pos_y, board_copy)
        self_copy.pos_x = pos_X
        self_copy.pos_y = pos_Y
        
        return is_check(self.side, board_copy) is False

    def move_to(self, pos_X : int, pos_Y : int, B: Board) -> Board:
        '''
        returns new board resulting from move of this knight to coordinates pos_X, pos_Y on board B 
        assumes this move is valid according to chess rules
        '''
        board_copy = (B[0], copy(B[1]))

        # Remove any enemy pieces.
        stationary_piece = get_piece_or_none(pos_X, pos_Y, board_copy)
        if stationary_piece is not None:
            board_copy[1].remove(stationary_piece)

        # Move the current piece.
        self.pos_x = pos_X
        self.pos_y = pos_Y

        return board_copy
        

class King(Piece):
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X, pos_Y, side_)

    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''checks if this king can move to coordinates pos_X, pos_Y on board B according to rule [Rule2] and [Rule3]'''
        # Implement rule 1.
        if (
                abs(self.pos_x-pos_X) > 1
                or abs(self.pos_y-pos_Y) > 1
                or abs(self.pos_x-pos_X)+abs(self.pos_y-pos_Y) <= 0
        ):
            return False
        
        # Implement rule 3.
        try:
            stationary_piece = get_piece_or_none(pos_X, pos_Y, B)
            if stationary_piece is None:
                return True
            return stationary_piece.side is not self.side
        except ValueError as e:
            # Handle edge cases.
            if e.args[0] == 'One of the coordinate is out of bounds.':
                return False

    def can_move_to(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''checks if this king can move to coordinates pos_X, pos_Y on board B according to all chess rules'''
        board_copy = deepcopy(B)

        if self.can_reach(pos_X, pos_Y, board_copy) is False:
            return False
        
        # Remove any enemy pieces.
        stationary_piece = get_piece_or_none(pos_X, pos_Y, board_copy)
        if stationary_piece is not None:
            # Move is immediately valid if king is eaten.
            if isinstance(stationary_piece, King) is True:
                return True
            board_copy[1].remove(stationary_piece)
        
        # Move the current piece.
        self_copy = piece_at(self.pos_x, self.pos_y, board_copy)
        self_copy.pos_x = pos_X
        self_copy.pos_y = pos_Y
        
        return is_check(self.side, board_copy) is False

    def move_to(self, pos_X : int, pos_Y : int, B: Board) -> Board:
        '''
        returns new board resulting from move of this king to coordinates pos_X, pos_Y on board B 
        assumes this move is valid according to chess rules
        '''
        board_copy = (B[0], copy(B[1]))

        # Remove any enemy pieces.
        stationary_piece = get_piece_or_none(pos_X, pos_Y, board_copy)
        if stationary_piece is not None:
            board_copy[1].remove(stationary_piece)

        # Move the current piece.
        self.pos_x = pos_X
        self.pos_y = pos_Y

        return board_copy


def get_king(side: bool, B: Board) -> King:
    for piece in B[1]:
        if isinstance(piece, King) is True and piece.side is side:
            return piece


def is_check(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is check for side
    Hint: use can_reach
    '''
    defending_king = get_king(side, B)

    for piece in B[1]:
        if piece.can_reach(defending_king.pos_x, defending_king.pos_y, B) is True:
            return True
        
    return False


def is_checkmate(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is checkmate for side

    Hints: 
    - use is_check
    - use can_reach 
    '''
    if is_check(side, B) is False:
        return False

    defending_king = get_king(side, B)

    surrounding_squares = (
        (column, row)
        for column in range(defending_king.pos_x-1, defending_king.pos_x+2)
        for row in range(defending_king.pos_y-1, defending_king.pos_y+2)
    )
    for surrounding_square in surrounding_squares:
        if defending_king.can_move_to(surrounding_square[0], surrounding_square[1], B) is True:
            return False
        
    # Cover the scenario where checking piece can be eaten.
    checking_piece = None
    for piece in B[1]:
        if piece.can_reach(defending_king.pos_x, defending_king.pos_y, B) is True:
            checking_piece = piece
            # There can only be one checking piece.
            break
    for piece in B[1]:
        if piece.can_reach(checking_piece.pos_x, checking_piece.pos_y, B) is True:
            return False
        
    return True


def is_stalemate(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is stalemate for side

    Hints: 
    - use is_check
    - use can_move_to 
    '''
    if is_check(side, B) is True:
        return False
    
    for piece in B[1]:
        if piece.side is side and isinstance(piece, King) is False:
            return False

    defending_king = get_king(side, B)

    surrounding_squares = (
        (column, row)
        for column in range(defending_king.pos_x-1, defending_king.pos_x+2)
        for row in range(defending_king.pos_y-1, defending_king.pos_y+2)
    )
    for surrounding_square in surrounding_squares:
        if defending_king.can_move_to(surrounding_square[0], surrounding_square[1], B) is True:
            return False
        
    return True


def read_board(filename: str) -> Board:
    '''
    reads board configuration from file in current directory in plain format
    raises IOError exception if file is not valid (see section Plain board configurations)
    '''
    lines = []
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise FileNotFoundError('File does not exist.')

    if len(lines) < 3:
        raise IOError('There are less than 3 lines in the file.')
    board_size = lines[0].strip()
    if board_size.isnumeric() is False:
        raise IOError('Board size is not an integer.')
    board_size = int(board_size)
    if board_size<3 or board_size>26:
        raise IOError('Board size is not within 3 to 26.')
    
    Side = namedtuple('Side', 'white black')
    side = Side(1, 2)
    for i in side:
        pieces = lines[i].strip().split(',')
        for piece in pieces:
            if piece[0] != 'N' or piece[0] != 'K':
                raise IOError('Piece type other than N or K was found.')


def save_board(filename: str, B: Board) -> None:
    '''saves board configuration into file in current directory in plain format'''


def find_black_move(B: Board) -> tuple[Piece, int, int]:
    '''
    returns (P, x, y) where a Black piece P can move on B to coordinates x,y according to chess rules 
    assumes there is at least one black piece that can move somewhere

    Hints: 
    - use methods of random library
    - use can_move_to
    '''


def conf2unicode(B: Board) -> str: 
    '''converts board cofiguration B to unicode format string (see section Unicode board configurations)'''


def main() -> None:
    '''
    runs the play

    Hint: implementation of this could start as follows:
    filename = input("File name for initial configuration: ")
    ...
    '''    


if __name__ == '__main__': #keep this in
   main()
