import math, copy

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
    """
    count = 0
    for line in board:
        for element in line:
            if element == EMPTY:
                count += 1
    if count == 0:
        return None
    elif count % 2 != 0:
        return X
    else:
        return O
    


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == EMPTY:
                actions.add((row, col))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # check if action is valid
    if action not in actions(board):
        raise Exception("invalid action")
    # make a deepcopy of the board
    board_copy = copy.deepcopy(board)
    # check who's turn it is
    symbol = player(board)
    # insert into the copy at the position given by action either X or 0
    board_copy[action[0]][action[1]] = symbol

    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    b = board
    # define list of columns and diagonals
    columns = [[b[i][0] for i in range(3)], [b[i][1] for i in range(3)], [b[i][2] for i in range(3)]]
    diagonals = [b[i][j] for i in range(3) for j in range(3) if i == j], [b[i][j] for i in range(3) for j in range(3) if i + j == 2]
    # loop through every row, col and diagonal and see if three Xs or Os are present
    for row in b:
        if any(row.count(k) == 3 for k in [X, O]):
            winner = [k for k in [X, O] if row.count(k) == 3][0]
            return winner
    for col in columns:
        if any(col.count(k) == 3 for k in [X, O]):
            winner = [k for k in [X, O] if col.count(k) == 3][0]
            return winner
    for diagonal in diagonals:
        if any(diagonal.count(k) == 3 for k in [X, O]):
            winner = [k for k in [X, O] if diagonal.count(k) == 3][0]
            return winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # if winner, return True
    if winner(board) in [X, O]:
        return True
    # loop and as soon as you find an EMPTY cell, return False
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    return True



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # define the agent
    agent = player(board)
    # if X, then define the max value of the board, else the min
    if agent == X:
        value = max_value(board)
        # among all options, pick the one with value = max_value
        for a in actions(board):
            if min_value(result(board, a)) == value:
                return a
    elif agent == O:
        value = min_value(board)
        # among all options, pick the one with value = min_value
        for a in actions(board):
            if max_value(result(board, a)) == value:
                return a


def max_value(board):
    v = -1000
    # base case
    if terminal(board):
        return utility(board)
    # recursion
    for a in actions(board):
        v = max(v, min_value(result(board, a)))

    return v


def min_value(board):
    v = 1000
    # base case
    if terminal(board):
        return utility(board)
    # recursion
    for a in actions(board):
        v = min(v, max_value(result(board, a)))
    return v
