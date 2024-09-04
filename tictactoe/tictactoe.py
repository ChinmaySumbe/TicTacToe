import math
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.

    It checks how many times X and O have played the moves, and assigns the chance to X if both have
    played otherwise, O
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count == o_count else O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    
    available_moves stores the cell of tic-tac board which can be considered for next move 
    """
    available_moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                available_moves.add((i, j))
    return available_moves

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    
    if player plays a move which is out of board's scope it raises an exception"""
    if action not in actions(board):
        raise ValueError("This is an invalid action")

    new_board_state = copy.deepcopy(board)
    current_player_mark = player(board)

    row, col = action
    new_board_state[row][col] = current_player_mark

    return new_board_state

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != EMPTY:
            return row[0]

    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != EMPTY:
            return board[0][col]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]

    return EMPTY

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # Player has won the game
    if winner(board) is not None:
        return True
    
    # No more moves left
    if all(cell != EMPTY for row in board for cell in row):
        return True
    
    return False

def utility(board):

    # Check if X has won
    if winner(board) == X:
        return 1
    # Check if O has won
    elif winner(board) == O:
        return -1
    # Otherwise, it's a tie
    else:
        return 0

def minimax(board):
    """
    The Minimax algorithm involves players alternating turns, aiming to maximize or minimize scores, 
    resulting in an iterative search for optimal moves.
    """
    def max_value(board):
        
        if terminal(board):
            return utility(board)
        
        v = -1000000
        for action in actions(board):
            v = max(v, min_value(result(board, action)))
        return v

    def min_value(board):
        if terminal(board):
            return utility(board)
        v = 1000000
        for action in actions(board):
            v = min(v, max_value(result(board, action)))
        return v

    # If the game is already over, return None (no valid move)
    if terminal(board):
        return None

    if player(board) == X:
        value, move = -math.inf, None
        for action in actions(board):
            n_val = min_value(result(board, action))
            if n_val > value:
                value, move = n_val, action
        return move
    else:
        value, move = math.inf, None
        for action in actions(board):
            n_val = max_value(result(board, action))
            if n_val < value:
                value, move = n_val, action
        return move