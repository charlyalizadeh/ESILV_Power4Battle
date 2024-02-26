import pathlib
from pathlib import Path
from os import system, name
import numpy as np
from collections import defaultdict
import time
import datetime
import pandas as pd

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')

def display_board(board, n_move, col):
    hl_move = False
    for i in range(6):
        for j in range(12):
            if board[i, j] == 1:
                if j == col and not hl_move:
                    print(f"{bcolors.FAIL}{bcolors.BOLD} X {bcolors.ENDC}", end='')
                    hl_move = True
                else:
                    print(" X ", end='')
            elif board[i, j] == -1:
                if j == col and not hl_move:
                    print(f"{bcolors.FAIL}{bcolors.BOLD} O {bcolors.ENDC}", end='')
                    hl_move = True
                else:
                    print(" O ", end='')
            else:
                print(" . ", end='')
        print()
    print("-----------------------------------")
    print(" 0  1  2  3  4  5  6  7  8  9 10 11")
    print(f"Number of token: {n_move}")

def choose_player(question):
    directories = [d for d in Path("./").iterdir() if str(d)[0] not in ('.', '_') and d.is_dir()]
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

def get_first_empty_row(col):
    elements = np.where(col == 0)
    if elements[0].size == 0:
        return -1
    else:
        return elements[0][-1]


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

def is_valid_col(board, col):
    if col is None or type(col) != int:
        return False
    if col < 0 or col > 11:
        return False
    if board[0][col] != 0:
        return False
    return True

def choose_ia_battle():
    clear()
    first_dir = choose_player("Please chose the first player (X):")
    clear()
    second_dir = choose_player("Please chose the second player (O):")
    clear()
    ia1 = __import__(f"{first_dir.name}")
    ia2 = __import__(f"{second_dir.name}")
    print(f"===== {first_dir} VS {second_dir} =====")
    battle(ia1, ia2, first_dir, second_dir)

def tournament(dirs):
    results = []
    for i in range(len(dirs)):
        for j in range(i + 1, len(dirs)):
            ia1 = __import__(f"{dirs[i].name}")
            ia2 = __import__(f"{dirs[j].name}")
            print(f"{dirs[i]} VS {dirs[j]}")
            result1 = battle(ia1, ia2, dirs[i], dirs[j], display=False, press_key=False)
            result2 = battle(ia2, ia1, dirs[j], dirs[i], display=False, press_key=False)
            if result2 == 1:
                result2 = 2
            elif result2 == 2:
                result2 = 1
            results.append([dirs[i], dirs[j], result1, result2])
    data = pd.DataFrame(results, columns=['Player 1', 'Player 2', 'Match 1', 'Match 2'])
    data.to_csv('tournament.csv')
    print(data)

def display_time_mean(time_ia1, time_ia2):
    if len(time_ia1) != 0:
        print(f"IA1 mean time: {sum(time_ia1) / len(time_ia1)}")
    if len(time_ia2) != 0:
        print(f"IA2 mean time: {sum(time_ia2) / len(time_ia2)}")

def battle(ia1, ia2, first_dir, second_dir, display=True, press_key=False):
    board = np.zeros((6, 12))
    ia1.minimax.init()
    ia2.minimax.init()
    time_ia1 = []
    time_ia2 = []
    n_move = 0
    while True:
        if display:
            print("=============================================")
            print(f"(X) {first_dir} playing...")
        t1 = time.time()
        coord1 = ia1.minimax_play()
        t2 = time.time()
        difference = t2 - t1
        if display:
            print(f"(X) {first_dir} played: {coord1} in {difference} seconds")
        time_ia1.append(difference)
        if not is_valid_col(board, coord1):
            if display:
                print(f"!! {first_dir} played an impossible move !!")
            display_time_mean(time_ia1, time_ia2)
            return 2
        n_move += 1
        board[get_first_empty_row(board[:, coord1]), coord1] = 1
        ia2.minimax.opponent_play(coord1)
        if display:
            display_board(board, n_move, coord1)
        state = check_win(board)
        if state == 1:
            if display:
                print(f"(X) {first_dir} wins !")
                display_time_mean(time_ia1, time_ia2)
            return 1
        elif state == -2:
            if display:
                print("Null game")
                display_time_mean(time_ia1, time_ia2)
            return 0
        if display:
            if press_key:
                input("==============Press a key====================\n\n")
            else:
                print("=============================================\n\n")
            print("=============================================")
            print(f"(O) {second_dir} playing...")
        t1 = time.time()
        coord2 = ia2.minimax_play()
        t2 = time.time()
        difference = t2 - t1
        if display:
            print(f"(O) {second_dir} played: {coord2} in {difference} seconds")
        time_ia2.append(difference)
        if not is_valid_col(board, coord2):
            if display:
                print(f"!! {second_dir} played an impossible move !!")
            display_time_mean(time_ia1, time_ia2)
            return 1
        n_move += 1
        board[get_first_empty_row(board[:, coord2]), coord2] = -1
        ia1.minimax.opponent_play(coord2)
        if display:
            display_board(board, n_move, coord2)
        if n_move == 42:
            if display:
                print("Null game")
                display_time_mean(time_ia1, time_ia2)
            return 0
        state = check_win(board)
        if state == -1:
            if display:
                print(f"(O) {second_dir} wins !")
                display_time_mean(time_ia1, time_ia2)
            return 2
        elif state == -2:
            if display:
                print("Null game")
                display_time_mean(time_ia1, time_ia2)
            return 0
        if display:
            if press_key:
                input("==============Press a key====================\n\n")
            else:
                print("=============================================\n\n")

# Tournament
#directories = [d for d in Path("./").iterdir() if str(d)[0] not in ('.', '_') and d.is_dir()]
#tournament(directories)

# Battle
choose_ia_battle()
