#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys
#import time
#import numpy as np
from copy import deepcopy

ROW = "ABCDEFGHI"
COL = "123456789"

row = [[False] * 9 for _ in range(9)]
column = [[False] * 9 for _ in range(9)]
block = [[[False] * 9 for _a in range(3)] for _b in range(3)]


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)

def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)

def initial(board):
    legal_values = {}
    for i in ROW:
        for j in COL:
            if board[i + j] == 0:
                legal_values[i + j] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            else:
                digit = board[i+j] - 1
                row[ord(i) - 65][digit] = True
                column[int(j) - 1][digit] = True
                block[(ord(i) - 65) // 3][(int(j) - 1) // 3][digit] = True
    return legal_values

def complete(board):
    for i in ROW:
        for j in COL:
            if board[i + j] == 0:
                return False
    return True

def heuristic(legal_values):
    minimum = 9
    pos = ""

    for key in legal_values:
        for value in legal_values[key]:
            r = ord(key[0]) - 65
            c = int(key[1]) - 1
            if row[r][value - 1] == True or column[c][value - 1] == True or block[r // 3][c // 3][value - 1] == True:
                legal_values[key].remove(value)

        if len(legal_values[key]) < minimum:
            minimum = len(legal_values[key])
            pos = key

    return pos, legal_values

def backtracking(board):
    """Takes a board and returns solved board."""
    # TODO: implement this
    legal_values = initial(board)
    solved_board = dfs(board, legal_values)
    return solved_board


def dfs(board, legal_values):
    if complete(board):
        return board

    board = deepcopy(board)
    legal_values = deepcopy(legal_values)
    pos, legal_values = heuristic(legal_values)
    values = legal_values.pop(pos)

    for i in values:
        board[pos] = i
        r = ord(pos[0]) - 65
        c = int(pos[1]) - 1
        if row[r][i - 1] == column[c][i - 1] == block[r // 3][c // 3][i - 1] == False:
            row[r][i - 1] = column[c][i - 1] = block[r // 3][c // 3][i - 1] = True
            result = dfs(board, legal_values)
            row[r][i - 1] = column[c][i - 1] = block[r // 3][c // 3][i - 1] = False
            if result != "failure":
                return result

    return "failure"


if __name__ == '__main__':

    if len(sys.argv) > 1:

        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = { ROW[r] + COL[c]: int(sys.argv[1][9*r+c])
                  for r in range(9) for c in range(9)}

        solved_board = backtracking(board)
        #print(board_to_string(solved_board))

        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py

        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        # Solve each board using backtracking
        #time_arr = []
        for line in sudoku_list.split("\n"):

            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = { ROW[r] + COL[c]: int(line[9*r+c])
                      for r in range(9) for c in range(9)}

            # Print starting board. TODO: Comment this out when timing runs.
            #print_board(board)

            # Solve with backtracking
            row = [[False] * 9 for _ in range(9)]
            column = [[False] * 9 for _ in range(9)]
            block = [[[False] * 9 for _a in range(3)] for _b in range(3)]

            #start_time = time.time()

            solved_board = backtracking(board)

            #end_time = time.time()
            #running_time = end_time - start_time
            #time_arr.append(running_time)

            # Print solved board. TODO: Comment this out when timing runs.
            #print_board(solved_board)

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')
        '''''
        with open('README.txt', 'w') as file:
            file.write('solved_boards: {}\n'.format(len(time_arr)))
            file.write('min: {}\n'.format(np.min(time_arr)))
            file.write('max: {}\n'.format(np.max(time_arr)))
            file.write('mean: {}\n'.format(np.mean(time_arr)))
            file.write('standard deviation: {}\n'.format(np.std(time_arr)))
        '''


        print("Finishing all boards in file.")