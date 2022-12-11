from pathlib import Path
from collections import defaultdict

def relative_path(filename):
    try:
        return f"{Path(__file__).parent.parent}\\2022_data\\{filename}.txt"
    except:
        return f'.\\2022_data\\{filename}.txt'

def read_data(filename):
    path = relative_path(filename)
    with open(file=path, mode='r') as data:
        raw = [d.replace('\n','') for d in data]
    grid = dict()
    for y, row in enumerate(raw):
        for x, tree in enumerate(row):
            grid[(x,y)] = int(tree)
    return grid

def is_visible(grid:dict, loc:tuple)->bool:
    height = grid[loc]
    x = loc[0]
    y = loc[1]
    rows = max([x[0] for x in grid.keys()])
    cols = max([x[1] for x in grid.keys()])
    #edges always visible
    is_visible = True if (min(x,y) == 0 or x == rows or y == cols) else False
    while not is_visible:
        if height > max([grid[(_x,y)] for _x in range(0,x)]):
            is_visible = True
        if height > max([grid[(_x,y)] for _x in range(x+1,cols+1)]):
            is_visible = True
        if height > max([grid[(x,_y)] for _y in range(0,y)]):
            is_visible = True
        if height > max([grid[(x,_y)] for _y in range(y+1,rows+1)]):
            is_visible = True
        return is_visible
    return is_visible

def count_left(grid, loc, rows, cols):
    x,y = loc
    height = grid[loc]
    count = 1
    if x == 0:
        return 0
    for _x in range(x-1,-1,-1):
        if height > grid[_x,y]:
            count += 1
        else:
            return count
    return count - 1

def count_right(grid, loc, rows, cols):
    x,y = loc
    height = grid[loc]
    count = 1
    if x == 0 or y == 0 or x == rows or y == cols:
        return 0
    for _x in range(x+1,cols+1,1):
        if height > grid[_x,y]:
            count += 1
        else:
            return count
    return count-1

def count_up(grid, loc, rows, cols):
    x,y = loc
    height = grid[loc]
    count = 1
    if x == 0 or y == 0 or x == rows or y == cols:
        return 0
    for _y in range(y-1,-1,-1):
        if height > grid[x,_y]:
            count += 1
        else:
            return count
    return count-1

def count_down(grid, loc, rows, cols):
    x,y = loc
    height = grid[loc]
    count = 1
    if x == 0 or y == 0 or x == rows or y == cols:
        return 0
    for _y in range(y+1,rows+1,1):
        if height > grid[x,_y]:
            count += 1
        else:
            return count
    return count-1

def score(grid):
    scores = dict()
    rows = max([x[0] for x in grid.keys()])
    cols = max([x[1] for x in grid.keys()])
    for loc in grid:
        score = 1
        while score > 0:
            score *= count_left(grid,loc,rows,cols)
            score *= count_right(grid,loc,rows,cols)
            score *= count_up(grid,loc,rows,cols)
            score *= count_down(grid,loc,rows,cols)
            break
        scores[loc] = score
    return scores

def part_one(filename):
    _map = read_data(filename)
    count = 0
    for tree in _map.keys():
        count += is_visible(_map, tree)
    return count

def part_two(filename):
    _map = read_data(filename)
    scores = score(_map)
    return max(scores.values())


if __name__ == '__main__':
    print(f"part one test: {part_one('day_8_test')}")
    print(f"part one: {part_one('day_8')}")
    print(f"part two test: {part_two('day_8_test')}")
    print(f"part two: {part_two('day_8')}")
