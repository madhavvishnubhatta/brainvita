import time
import copy
import argparse
import json
import os

full_board = []
full_board.append([-1, -1,  1,  1,  1, -1, -1])
full_board.append([-1, -1,  1,  1,  1, -1, -1])
full_board.append([ 1,  1,  1,  1,  1,  1,  1])
full_board.append([ 1,  1,  1,  0,  1,  1,  1])
full_board.append([ 1,  1,  1,  1,  1,  1,  1])
full_board.append([-1, -1,  1,  1,  1, -1, -1])
full_board.append([-1, -1,  1,  1,  1, -1, -1])

solutions = []
moves = []

solutions_file_name = 'solutions.json'

def count_marbles(board):
    count = 0
    for row in board:
        for cell in row:
            if cell == 1:
                count = count+1
    return count

def print_board(board):
    for row in board:
        for cell in row:
            if cell == 1:
                print("1",end=" ")
            elif cell == -1:
                print(" ",end=" ")
            elif cell == 0:
                print("-",end=" ")
        print("")

marble_counter = 32

max_reached = False
def solve(board):

    marbles_count = count_marbles(board)

    if marbles_count == 1:
        #Found a solution. Add moves to the list of solutions
        solution = copy.deepcopy(moves)
        solutions.append(solution)
        print(f"Solutions computed: {len(solutions)}", end = '\r')
        if len(solutions) == args.max_solutions:
            return True #End calculating solutions
        else:
            return False
    else:
        possible_moves = find_all_possible_moves(board)
        if len(possible_moves) == 0: #No solution possibe down this path
            return False
        else:
            for move in possible_moves:
                moves.append(move)
                apply_move(board,move)
                if solve(board):
                    return True
                moves.pop()
                unapply_move(board,move)

#def apply(board,move):

def is_valid_cell(i,j):
    if i < 0 or i > 6:
        return False
    elif j < 0 or j > 6:
        return False
    elif i in [0,1,5,6] and j in [0,1,5,6]:
        return False
    else:
        return True

def is_there_valid_left_move(board, i,j):
    if is_valid_cell(i,j-1) and is_valid_cell(i,j-2):
        if board[i][j] == 1 and board[i][j-1] ==1 and board[i][j-2] == 0:
            return True
    return False

def is_there_valid_right_move(board,i,j):
    if is_valid_cell(i,j+1) and is_valid_cell(i,j+2):
        if board[i][j] == 1 and board[i][j+1] ==1 and board[i][j+2] == 0:
            return True
    return False

def is_there_valid_up_move(board, i,j):
    if is_valid_cell(i-1,j) and is_valid_cell(i-2,j):
        if board[i][j] == 1 and board[i-1][j] ==1 and board[i-2][j] == 0:
            return True
    return False

def is_there_valid_down_move(board,i,j):
    if is_valid_cell(i+1,j) and is_valid_cell(i+2,j):
        if board[i][j] == 1 and board[i+1][j] ==1 and board[i+2][j] == 0:
            return True
    return False

def apply_move(board, move):
    i = move['row']
    j = move['col']
    board[i][j] = 0
    if move['direction'] == 'left':
        board[i][j-1] = 0
        board[i][j-2] = 1
    elif move['direction'] == 'right':
        board[i][j+1] = 0
        board[i][j+2] = 1
    elif move['direction'] == 'up':
        board[i-1][j] = 0
        board[i-2][j] = 1
    elif move['direction'] == 'down':
        board[i+1][j] = 0
        board[i+2][j] = 1

def unapply_move(board, move):
    i = move['row']
    j = move['col']
    board[i][j] = 1
    if move['direction'] == 'left':
        board[i][j-1] = 1
        board[i][j-2] = 0
    elif move['direction'] == 'right':
        board[i][j+1] = 1
        board[i][j+2] = 0
    elif move['direction'] == 'up':
        board[i-1][j] = 1
        board[i-2][j] = 0
    elif move['direction'] == 'down':
        board[i+1][j] = 1
        board[i+2][j] = 0

def apply_and_display_move(board, move):
    apply_move(board,move)
    UP = '\033[1A'
    CLEAR = '\x1b[2K'
    #Clear board display
    for i in range(7):
        print(UP, end=CLEAR)
    print_board(board)

def find_all_possible_moves(board):
    possible_moves = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if not is_valid_cell(i,j):
                continue
            else:
                if is_there_valid_left_move(board,i,j):
                    possible_moves.append({'row':i, 'col':j, 'direction':'left'})
                if is_there_valid_right_move(board,i,j):
                    possible_moves.append({'row':i, 'col':j, 'direction':'right'})
                if is_there_valid_up_move(board,i,j):
                    possible_moves.append({'row':i, 'col':j, 'direction':'up'})
                if is_there_valid_down_move(board,i,j):
                    possible_moves.append({'row':i, 'col':j, 'direction':'down'})
    return possible_moves

def copy_board(board):
    copy = []
    for i in range(len(board)):
        copy.append([])
        for j in range(len(board[i])):
            copy[i].append(board[i][j])
    return copy

def write_solutions_to_file():
    with open('solutions.json', 'w') as fout:
        json.dump(solutions, fout, indent = 4)

def read_solutions_from_file():
    print("Reading solutions from file")
    with open(solutions_file_name, 'r') as fin:
        solutions.extend(json.load(fin))

parser = argparse.ArgumentParser(description='Generate Solutions to the "Brainvita" puzzle')
parser.add_argument("--max_solutions", type=int,
                    default = 100,
                    help = 'Maximum number of solutions to look for. There are tens of thousands of solutions. So please specify a number at which point the script will stop. The default is 100')
parser.add_argument("--solution_num", type=int,
                    default = 1,
                    help = 'The solution number to display')
parser.add_argument('--compute_solutions', action='store_true', dest='compute_solutions',
                    default=False,
                    help='''If you use this flag, the solutions will be computed. If not specified, then it will be read from the file solutions.json''')
args = parser.parse_args()

full_board_copy = copy.deepcopy(full_board)

if not args.compute_solutions and os.path.isfile(solutions_file_name): #If compute solutions is not provided and the solutions file exists, then read the solutions from it. If not, compute the solutions.
    read_solutions_from_file()
else:    
    solve(full_board)
    write_solutions_to_file()

print(f"\nFound {len(solutions)} solutions.")

print(f"Showing Solution: {args.solution_num}")
print_board(full_board_copy)
time.sleep(1)
solution = solutions[args.solution_num-1]
for move in solution:
    time.sleep(1)
    apply_and_display_move(full_board_copy, move)
