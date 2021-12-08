from os import sep
from pathlib import Path
import numpy as np

def relative_path(filename):
    try:
        return f"{Path(__file__).parent.parent.parent}\\data\\{filename}.txt"
    except:
        return f'.\\data\\{filename}.txt'

class bingo_board:
    def __init__(self, board_as_list) -> None:
        self.dim = len(board_as_list)
        self.board = np.array(board_as_list)
        self.tracker = np.zeros((self.dim,self.dim))
        self.called_values = []

    def call_number(self, num):
        location  = np.where(self.board == num)
        if len(location[0]) > 0:
            if num not in self.called_values:
                self.called_values.append(num)
            coords = list(zip(location[0],location[1]))
            for c in coords:
                self.tracker[c] = 1
        
    def check_for_winner(self):
        if np.isin(self.dim, self.tracker.sum(axis=1)):
            return True
        if np.isin(self.dim, self.tracker.sum(axis=0)):
            return True
        return False


def part_one(filename):
    path = relative_path(filename)
    with open(file=path, mode='r') as data:
        d = [line for line in data]
    key = [int(x) for x in d[0].split(',')]
    boards = []
    newboard = []
    for b in d[1:]:
        if b =='\n':
            if len(newboard) > 0:
                boards.append(newboard)
            newboard = []
        else:
            newboard.append([int(x) for x in b.split(' ') if x !=''])
    boards.append(newboard)
    boards = [bingo_board(b) for b in boards]

    for num in key:
        for board in boards:
            board.call_number(num)
            if board.check_for_winner():
                return (board.board.sum() - sum(board.called_values)) * board.called_values[-1]
    return 0

def part_two(filename):
    path = relative_path(filename)
    with open(file=path, mode='r') as data:
        d = [line for line in data]
    key = [int(x) for x in d[0].split(',')]
    boards = []
    newboard = []
    for b in d[1:]:
        if b =='\n':
            if len(newboard) > 0:
                boards.append(newboard)
            newboard = []
        else:
            newboard.append([int(x) for x in b.split(' ') if x !=''])
    boards.append(newboard)
    boards = [bingo_board(b) for b in boards]
    finishedboards = []
    for num in key:
        for i, b in enumerate(boards):
            if i in finishedboards:
                pass
            else:
                b.call_number(num)
                if b.check_for_winner():
                    finishedboards.append(i)
    lastfinished = finishedboards[-1]
    board = boards[lastfinished]
    return (board.board.sum() - sum(board.called_values)) * board.called_values[-1]
    
if __name__ == '__main__':
    print(f"part one test: {part_one('day_4_test')}")
    print(f"part one: {part_one('day_4')}")
    print(f"part two test: {part_two('day_4_test')}")
    print(f"part two: {part_two('day_4')}")