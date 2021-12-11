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
        heightmap = {}
        heightlist = [d for d in data]
        y_max = len(heightlist) - 1
        for y, line in enumerate(heightlist):
            for x, height in enumerate(line.replace('\n','')):
                heightmap[(x,y_max - y)] = int(height)
    return heightmap

def find_lowpoints(heightmap):
    low_points = {}
    for key, value in heightmap.items():
        x, y = key
        try:
            if heightmap[(x+1,y)] <= value:
                continue
        except KeyError:
            pass
        try:
            if heightmap[(x-1,y)] <= value:
                continue
        except KeyError:
            pass        
        try:
            if heightmap[(x,y+1)] <= value:
                continue
        except KeyError:
            pass
        try:
            if heightmap[(x,y-1)] <= value:
                continue
        except KeyError:
            pass
        low_points[(x,y)] = value
    return low_points

def part_one(filename):
    heightmap = get_data(filename)
    lows = find_lowpoints(heightmap)
    sum = 0
    for key, value in lows.items():
        sum += (value+1)
    return sum

def count_right(heightmap, coord):
    coords = []
    x,y = coord
    value = heightmap[(coord)]
    try:
        if value <= heightmap[(x+1, y)] < 9:
            coords.append([x+1,y])
            coords += list(count_right(heightmap, (x+1, y)))
            coords += list(count_above(heightmap, (x+1, y)))
            coords += list(count_below(heightmap, (x+1, y)))
    except KeyError:
        return coords
    return coords    

def count_left(heightmap, coord):
    coords = []
    x,y = coord
    value = heightmap[(coord)]
    try:
        if value <= heightmap[(x-1, y)] < 9:
            coords.append([x-1,y])
            coords += list(count_left(heightmap, (x-1, y)))
            coords += list(count_above(heightmap, (x-1, y)))
            coords += list(count_below(heightmap, (x-1, y)))
    except KeyError:
        return coords
    return coords

def count_above(heightmap, coord):
    coords = []
    x,y = coord
    value = heightmap[(coord)]
    try:
        if value <= heightmap[(x, y+1)] < 9:
            coords.append([x,y+1])
            coords += list(count_above(heightmap, (x, y+1)))
            coords += list(count_right(heightmap, (x, y+1)))
            coords += list(count_left(heightmap, (x, y+1)))
    except KeyError:
        return coords
    return coords

def count_below(heightmap, coord):
    coords = []
    x,y = coord
    value = heightmap[(coord)]
    try:
        if value <= heightmap[(x, y-1)] < 9:
            coords.append([x,y-1])
            coords += list(count_below(heightmap, (x, y-1)))
            coords += list(count_right(heightmap, (x, y-1)))
            coords += list(count_left(heightmap, (x, y-1)))
    except KeyError:
        return coords
    return coords

def map_basin(heightmap, coord):
    x,y = coord
    origin = [x,y]
    left = count_left(heightmap, coord)
    right = count_right(heightmap, coord)
    above = count_above(heightmap, coord)
    below = count_below(heightmap, coord)

    basin = left + above + right + below + [origin]
    basin = set([(x,y) for x,y in basin])
    return len(basin)

def part_two(filename):
    heightmap = get_data(filename)
    lows = find_lowpoints(heightmap)
    basins = []
    for low in lows:
        basin_size = map_basin(heightmap, low)
        basins.append(basin_size)
    basins.sort(reverse=True)
    return basins[0] * basins[1] * basins[2]

if __name__ == '__main__':
    print(f"part one test: {part_one('day_9_test')}")
    print(f"part one: {part_one('day_9')}")
    print(f"part two test: {part_two('day_9_test')}")
    print(f"part two: {part_two('day_9')}")