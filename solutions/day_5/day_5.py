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
        d = [line.split('->') for line in data]
        coords = [[eval(point) for point in cords] for cords in d]
    return coords

def part_one(filename):
    vectors = get_data(filename)
    vent_map = {}
    for start, end in vectors:
        x1,y1 = start
        x2,y2 = end
        if x1 == x2 or y1 == y2:
            for x in range(min(x1,x2),max(x1,x2)+1):
                for y in range(min(y1,y2),max(y1,y2)+1):
                    vent_map[(x,y)] = vent_map.get((x,y),0)+1
    danger = 0
    for key, value in vent_map.items():
        if value > 1:
            danger += 1    
    return danger


def part_two(filename):
    vectors = get_data(filename)
    vent_map = {}
    for start, end in vectors:
        x1,y1 = start
        x2,y2 = end
        if x1 == x2 or y1 == y2:
            for x in range(min(x1,x2),max(x1,x2)+1):
                for y in range(min(y1,y2),max(y1,y2)+1):
                    vent_map[(x,y)] = vent_map.get((x,y),0)+1
        elif abs(x2-x1) == abs(y2-y1):
            print(f'start: {start}: end {end}')
            x_range = range(x1,x2+1 if x2>x1 else x2-1, 1 if x2>x1 else -1)
            y_range = range(y1,y2+1 if y2>y1 else y2-1, 1 if y2>y1 else -1)
            diag = zip(x_range, y_range)
            for x,y in diag:
                vent_map[(x, y)] = vent_map.get((x,y),0)+1
    danger = 0
    for key, value in vent_map.items():
        if value > 1:
            danger += 1    
    return danger

if __name__ == '__main__':
    print(f"part one test: {part_one('day_5_test')}")
    print(f"part one: {part_one('day_5')}")
    print(f"part two test: {part_two('day_5_test')}")
    print(f"part two: {part_two('day_5')}")