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
    # The format must be a tuple `action` with:
    #   - action[0]: the row coordinate
    #   - action[1]: the column coordinate

    # Here the exemple plays the first empty square
    empty = np.where(my_board.board == 0)
    action = (empty[0][0], empty[1][0])
    my_board.board[action[0], action[1]] = 1 # !! DONT FORGET TO PLAY AND THEN RETURN THE MOVE YOU PLAYED !!
    return action

def opponent_play(action):
    # The opponent plays
    # The format of `action` is the same as in `minimax_play`
    my_board.board[action[0], action[1]] = -1
