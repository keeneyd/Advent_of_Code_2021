from os import sep
from pathlib import Path

def relative_path(filename):
    try:
        return f"{Path(__file__).parent.parent.parent}\\data\\{filename}.txt"
    except:
        return f'.\\data\\{filename}.txt'

def get_data(filename):
    path = relative_path(filename)
    with open(file=path, mode='r') as data:
        data = [d for d in data]
        lines = [d.replace('\n','') for d in data if not d.startswith('fold')]
        lines = [line.split(',') for line in lines[:-1] ]
        lines = [tuple([int(l) for l in line]) for line in lines]

        folds = [d.replace('fold along ','').replace('\n','').split('=') for d in data if d.startswith('fold')]
    return lines, folds

class folding_paper:
    def __init__(self, coords):
        self.grid = {c : 1 for c in coords}
        self.height = 0
        self.width = 0
        self.set_dimensions()

    def set_dimensions(self):
        height = 0
        width = 0
        for x,y in self.grid:
            height = y if y > height else height
            width = x if x > width else width
        self.height = height
        self.width =width

    def horizontal_fold(self, fold_line):
        new_grid = {}
        for x,y in self.grid:
            if y < fold_line:
                new_grid[(x,y)] = 1
            else:
                new_grid[(x,self.height - y)] = 1
        self.grid = new_grid
        self.set_dimensions()

    def vertical_fold(self, fold_line):
        new_grid = {}
        for x,y in self.grid:
            if x < fold_line:
                new_grid[(x,y)] = 1
            else:
                new_grid[(self.width -x, y)] = 1
        self.grid = new_grid
        self.set_dimensions()

    def __repr__(self) -> str:
        output = ''
        for y in range(self.height+1):
            for x in range(self.width+1):
                if self.grid.get((x,y),0) > 0:
                    output += '#'
                else:
                    output += '.'
            output += "\n"
        return output

def part_one(filename):
    lines, folds = get_data(filename)
    paper = folding_paper(lines)
    direction, line = folds[0]
    if direction == 'y':
        paper.horizontal_fold(int(line))
    if direction == 'x':
        paper.vertical_fold(int(line))
    return len(paper.grid)

def part_two(filename):
    lines, folds = get_data(filename)
    paper = folding_paper(lines)
    for fold in folds:
        direction, line = fold
        if direction == 'y':
            paper.horizontal_fold(int(line))
        if direction == 'x':
            paper.vertical_fold(int(line))
    print(paper)
    return None

if __name__ == '__main__':
    print(f"part one test: {part_one('day_13_test')}")
    print(f"part one: {part_one('day_13')}")
    print(f"part two test: {part_two('day_13_test')}")
    print(f"part two: {part_two('day_13')}")