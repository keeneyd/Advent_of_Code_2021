from os import sep
from pathlib import Path
from collections import defaultdict, Counter

def relative_path(filename):
    try:
        return f"{Path(__file__).parent.parent.parent}\\data\\{filename}.txt"
    except:
        return f'.\\data\\{filename}.txt'

def get_data(filename):
    path = relative_path(filename)
    with open(file=path, mode='r') as data:
        data = [list(d.replace('\n','')) for d in data]        
        grid = {}
        max_y = len(data) -1
        max_x = len(data[0]) -1
        for y, row in enumerate(data):
            for x, val in enumerate(row):
                if val != '.':
                    grid[(x,max_y - y)] = val    
    return grid, max_x, max_y

def move_east(grid: dict, max_x: int, max_y: int) -> dict:
    new_grid = {}
    moves = 0
    for (x,y), cuke in grid.items():
        if cuke == '>':
            _x = 0 if x == max_x else x+1
            _y = y
            if not grid.get((_x,_y)):
                moves += 1
                new_grid[(_x,_y)] = cuke
            else: 
                new_grid[(x,y)] = cuke
        if cuke == 'v':
            new_grid[(x,y)] = cuke
    return new_grid, moves

def move_south(grid: dict, max_x: int, max_y: int) -> dict:
    new_grid = {}
    moves = 0
    for (x,y), cuke in grid.items():
        if cuke == 'v':
            _x = x
            _y = max_y if y == 0 else y - 1
            if not grid.get((_x,_y)):
                moves += 1
                new_grid[(_x,_y)] = cuke
            else: 
                new_grid[(x,y)] = cuke
        if cuke == '>':
            new_grid[(x,y)] = cuke
    return new_grid, moves

def part_one(filename):
    grid, max_x, max_y = get_data(filename)
    moves = 1
    turns = 0
    while moves > 0:
        turns += 1
        east_grid, east_moves = move_east(grid, max_x, max_y)
        grid, south_moves = move_south(east_grid, max_x, max_y)
        moves = east_moves + south_moves        
    return turns

if __name__ == '__main__':
    print(f"part one test: {part_one('day_25_test')}")
    print(f"part one: {part_one('day_25')}")