"""
Tic Tac Toe Player
"""

from copy import deepcopy
from curses.ascii import EM
import math
from queue import Empty

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
    x_count = 0
    o_count = 0

    if terminal(board):
        return None

    for row in board:
        for col in row:
            if col == X:
                x_count += 1
            elif col == O:
                o_count += 1

    if x_count == 0 or x_count == o_count:
        return X

    return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    moves = set()

    if terminal(board):
        return None

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                moves.add((i, j))

    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception('Not a valid action')

    new_board = deepcopy(board)

    new_board[action[0]][action[1]] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #checks in rows
    for row in board:
        if row[0] == row[1] == row[2]:
            return row[0]

    #checks in cols
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i]:
            return board[0][i]

    #checks in diagonals
    mid_cell = board[1][1]

    if board[0][0] == mid_cell == board[2][2]:
        return mid_cell

    if board[0][-1] == mid_cell == board[2][0]:
        return mid_cell

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    game_has_winner = winner(board)

    if game_has_winner is not None:
        return True

    for row in board:
        for col in row:
            if col == EMPTY:
                return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    w = winner(board)

    if w == X:
        return 1
    elif w == O:
        return -1

    return 0


def min_value(board):
    v = float('inf')

    if terminal(board):
        return utility(board)

    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    return v


def max_value(board):
    v = float('-inf')

    if terminal(board):
        return utility(board)

    for action in actions(board):
        v = max(v, min_value(result(board, action)))

    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None

    p = player(board)

    if p == X:
        best_result = float('-inf')

        for action in actions(board):
            play_result = min_value(result(board, action))

            if play_result > best_result:
                best_result = play_result
                best_move = action

    else:
        best_result = float('inf')

        for action in actions(board):
            play_result = max_value(result(board, action))

            if play_result < best_result:
                best_result = play_result
                best_move = action

    return best_move
