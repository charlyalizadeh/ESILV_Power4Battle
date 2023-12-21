# Template
import numpy as np

class MyBoard:
    def __init__(self):
        self.board = np.array([])

my_board = MyBoard()

def init():
    # Here put everything you need to initialize your IA
    my_board.board = np.zeros((6, 12))

def minimax_play():
    # Your IA plays and return the actioninate it played
    # Action must the index of the column you played (between 0 and 11)

    # Here the exemple plays the first column with an empty square
    for i in range(12):
        if np.where(my_board.board[:, i] == 0)[0].size != 0:
            return i
    return -1

def get_first_empty_row(col):
    elements = np.where(col == 0)
    if elements[0].size == 0:
        return -1
    else:
        return elements[0][-1]

def opponent_play(action):
    # The opponent plays
    # The format of `action` is the same as in `minimax_play`
    my_board.board[get_first_empty_row(my_board.board[:, action]), action] = -1
