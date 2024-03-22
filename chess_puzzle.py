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
        board_copy = deepcopy(B)

        # Remove any enemy pieces.
        stationary_piece = get_piece_or_none(pos_X, pos_Y, board_copy)
        if stationary_piece is not None:
            board_copy[1].remove(stationary_piece)

        # Move the current piece.
        self_copy = piece_at(self.pos_x, self.pos_y, board_copy)
        self_copy.pos_x = pos_X
        self_copy.pos_y = pos_Y

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
        board_copy = deepcopy(B)

        # Remove any enemy pieces.
        stationary_piece = get_piece_or_none(pos_X, pos_Y, board_copy)
        if stationary_piece is not None:
            board_copy[1].remove(stationary_piece)

        # Move the current piece.
        self_copy = piece_at(self.pos_x, self.pos_y, board_copy)
        self_copy.pos_x = pos_X
        self_copy.pos_y = pos_Y

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
    
    # Validate the lines.
    if len(lines) < 3:
        raise IOError('There are less than 3 lines in the file.')
    # Process each line - any spaces are not required for constructing the board.
    for i in range(len(lines)):
        lines[i] = lines[i].strip().replace(' ', '')

    # Validate the board size.
    board_size = lines[0]
    if board_size.isnumeric() is False:
        raise IOError('Board size is not an integer.')
    board_size = int(board_size)
    if board_size<3 or board_size>26:
        raise IOError('Board size is not within 3 to 26.')
    
    # Start building the board with the validated board size
    # and append the pieces next.
    board = (board_size, [])

    unique_indices = set()
    Side = namedtuple('Side', 'white black')
    side = Side(1, 2)
    for i in side:
        king_exists = False
        pieces = lines[i].split(',')
        for piece in pieces:
            # Validate the piece type.
            if piece == '':
                raise IOError('Piece type is empty.')
            piece_type = piece[0]
            if piece_type != 'N' and piece_type != 'K':
                raise IOError('Piece type other than N or K was found.')
            elif piece_type == 'K':
                if king_exists is True:
                    raise IOError('At least one side contains more than 1 king.')
                else:
                    king_exists = True
            # Validate the piece's column and row.
            indices = None
            try:
                indices = location2index(piece[1:])
            except ValueError as e:
                raise IOError(e.args[0])
            column, row = indices[0], indices[1]
            if column<1 or column>board_size:
                raise IOError('Column is not within 1 to max board size.')
            if row<1 or row>board_size:
                raise IOError('Row is not within 1 to max board size.')
            if indices in unique_indices:
                raise IOError('There are pieces in the same location.')
            else:
                unique_indices.add(indices)
            
            # Build the list of pieces in the board.
            if piece_type == 'N':
                board[1].append(Knight(column, row, i==side.white))
            elif piece_type == 'K':
                board[1].append(King(column, row, i==side.white))
            
    return board


def save_board(filename: str, B: Board) -> None:
    '''saves board configuration into file in current directory in plain format'''
    board_config = conf2unicode(B)

    with open(filename, 'w') as f:
        f.writelines(board_config)


def find_black_move(B: Board) -> tuple[Piece, int, int]:
    '''
    returns (P, x, y) where a Black piece P can move on B to coordinates x,y according to chess rules 
    assumes there is at least one black piece that can move somewhere

    Hints: 
    - use methods of random library
    - use can_move_to
    '''


def get_unicode_character(piece: Piece) -> str:
    '''Return the chess piece's unicode after reading the type and side.'''
    if isinstance(piece, Knight) is True:
        if piece.side is True:
            return '\u2658'
        else:
            return '\u265E'
    elif isinstance(piece, King) is True:
        if piece.side is True:
            return '\u2654'
        else:
            return '\u265A'


def conf2unicode(B: Board) -> str: 
    '''converts board cofiguration B to unicode format string (see section Unicode board configurations)'''
    # Initialise a grid of empty spaces with the rows reversed.
    grid = [['\u2001']*B[0] for _ in range(B[0])]

    # Fill occupied spaces with unicode chess pieces.
    for piece in B[1]:
        grid[piece.pos_y-1][piece.pos_x-1] = get_unicode_character(piece)

    board_config = ''
    # Since the rows are reversed, access them in reverse.
    for i in range(B[0]-1, -1, -1):
        board_config += ''.join(grid[i]) + '\n'
    
    return board_config


def parse_input_move(input_move: str) -> tuple[str, str]:
    '''Split the move input into the current location and destination.'''
    if int(len(input_move)%2) == 0:
        return (input_move[:int(len(input_move)/2)], input_move[int(len(input_move)/2):])
    
    from_move = input_move[0:2]
    to_move = ''
    if input_move[2].isnumeric is True:
        from_move += input_move[2]
        to_move = input_move[3:]
    else:
        to_move = input_move[2:]

    return (from_move, to_move)


def main() -> None:
    '''
    runs the play

    Hint: implementation of this could start as follows:
    filename = input("File name for initial configuration: ")
    ...
    '''
    filename = input('File name for initial configuration: ')
    board = None
    is_file_valid = False
    while is_file_valid is False:
        if filename == 'QUIT':
            return
        try:
            board = read_board(filename)
            is_file_valid = True
            print('The initial configuration is:')
            print(conf2unicode(board))
        except FileNotFoundError:
            filename = input('This is not a valid file. File name for initial configuration: ')
        except IOError:
            filename = input('This is not a valid file. File name for initial configuration: ')

    whose_turn = 'White'
    is_quitting = False
    while is_quitting is False:
        whose_turn = 'White'
        is_move_valid = False
        if whose_turn == 'White':
            move = input(f'Next move of {whose_turn}: ')
            while is_move_valid is False:
                if move == 'QUIT':
                    filename = input('File name to store the configuration: ')
                    save_board(filename, board)
                    print('The game configuration saved.')
                    return
                from_to = parse_input_move(move)
                piece = None
                try:
                    piece_indices = location2index(from_to[0])
                    destination_indices = location2index(from_to[1])
                    piece = get_piece_or_none(piece_indices[0], piece_indices[1], board)
                    if piece is None:
                        raise TypeError('No piece in the specified location.')
                    if piece.can_move_to(destination_indices[0], destination_indices[1], board) is False:
                        raise ValueError('The destination is invalid.')
                    is_move_valid = True
                except Exception as e:
                    move = input(f'This is not a valid move. Next move of {whose_turn}: ')
        else:
            move = find_black_move()
            print(f'Next move of Black is {move}. ', end='')

        piece.move_to(destination_indices[0], destination_indices[1], board)
        print(f"The configuration after {whose_turn}'s move is:")
        print(conf2unicode(board))
        if is_checkmate(whose_turn!='White', board) is True:
            print(f'Game over. {whose_turn} wins.')
            return
        if is_stalemate(whose_turn!='White', board) is True:
            print(f'Game over. Stalemate.')
            return
        if whose_turn == 'White':
            whose_turn == 'Black'
        else:
            whose_turn == 'White'


if __name__ == '__main__': #keep this in
   main()
