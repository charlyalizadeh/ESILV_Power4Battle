import pathlib
from pathlib import Path
from os import system, name
import numpy as np
from collections import defaultdict

def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')

def display_board(board):
    for i in range(6):
        for j in range(12):
            if board[i, j] == 1:
                print(" X ", end='')
            elif board[i, j] == -1:
                print(" O ", end='')
            else:
                print(" . ", end='')
        print()

def choose_player(question):
    directories = [d for d in Path("./").iterdir()]
    while True:
        print(question)
        for i, d in enumerate(directories):
            print(f"  {i}. {d.name}")
        ia_dir_index = int(input("Enter a number:"))
        if ia_dir_index < 0 or ia_dir_index >= len(directories):
            print("Please enter a valid number.")
        else:
            ia_dir = directories[ia_dir_index]
            break
    return ia_dir

def get_dict_occ(arr):
    unique, counts = np.unique(arr, return_counts=True)
    result = defaultdict(lambda: 0)
    result.update(dict(zip(unique, counts)))
    return result

def sublist(lst1, lst2):
    for i in range(len(lst2)):
        if len(lst2) - i < len(lst1):
            return False
        if lst2[i] == lst1[0]:
            j = 0
            while j < len(lst1) and lst1[j] == lst2[i + j]:
                j += 1
            if j == len(lst1):
                return True





def check_win(board):
    # Row
    for row in board:
        if sublist([1, 1, 1, 1], row.tolist()):
            return 1
        elif sublist([-1, -1, -1, -1], row.tolist()):
            return -1

    # Col
    for col in board.T:
        if sublist([1, 1, 1, 1], col.tolist()):
            return 1
        elif sublist([-1, -1, -1, -1], col.tolist()):
            return -1

    diags = [board[::-1,:].diagonal(i) for i in range(-board.shape[0]+1,board.shape[1])]
    board90 = np.rot90(board)
    diags.extend([board90[::-1,:].diagonal(i) for i in range(-board.shape[0]+1,board.shape[1])])
    for d in diags:
        if sublist([1, 1, 1, 1], d.tolist()):
            return 1
        elif sublist([-1, -1, -1, -1], d.tolist()):
            return -1

    if np.where(board == 0)[0].size == 0:
        return -2

    return 0



clear()
first_dir = choose_player("Please chose the first player (X):")
clear()
second_dir = choose_player("Please chose the second player (O):")
clear()
ia1 = __import__(f"{first_dir.name}")
ia2 = __import__(f"{second_dir.name}")
print(f"{first_dir} VS {second_dir}")
board = np.zeros((6, 12))
ia1.minimax.init()
ia2.minimax.init()
display_board(board)
while True:
    print(f"{first_dir} playing...")
    coord1 = ia1.minimax_play()
    print(f"Played: {coord1}")
    board[coord1[0], coord1[1]] = 1
    ia2.minimax.opponent_play(coord1)
    display_board(board)
    state = check_win(board)
    if state == 1:
        print(f"{first_dir} wins !")
        break
    elif state == -2:
        print("Null game")
        break
    input()
    print(f"{second_dir} playing...")
    coord2 = ia2.minimax_play()
    print(f"Played: {coord2}")
    board[coord2[0], coord2[1]] = -1
    ia1.minimax.opponent_play(coord2)
    display_board(board)
    state = check_win(board)
    if state == -1:
        print(f"{second_dir} wins !")
        break
    elif state == -2:
        print("Null game")
        break
    input()
