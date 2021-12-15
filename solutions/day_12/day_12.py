from os import sep
from pathlib import Path
from collections import defaultdict

def relative_path(filename):
    try:
        return f"{Path(__file__).parent.parent.parent}\\data\\{filename}.txt"
    except:
        return f'.\\data\\{filename}.txt'

def get_data(filename):
    path = relative_path(filename)
    with open(file=path, mode='r') as data:
        lines = [d.replace('\n','').split('-') for d in data]
        options = defaultdict(list)
        for key, value in lines:
            existing_value = options.get(key,[])
            existing_value.append(value)
            options[key] = existing_value

            if key != 'start':
                reverse_value = options.get(value,[])
                reverse_value.append(key)
                options[value] = reverse_value
    return options

def path_count(map, path=['start']):
    count = 0
    for point in map[path[-1]]:
        if point.isupper() or not point in path:
            count += 1 if point == 'end' else path_count(map, path + [point])
    return count

def alt_count(map, path=['start']):
    count = 0
    if double_small(path):
        for point in map[path[-1]]:
            if point.isupper() or not point in path:
                count += 1 if point == 'end' else path_count(map, path + [point])
    else:
        for point in map[path[-1]]:
            if point == 'end':
                count += 1
            elif point != 'start':
                count += alt_count(map, path + [point])
    return count

def double_small(path):
    smalls = {}
    for p in path:
        if p.islower():
            count = smalls.get(p,0)
            if count > 0:
                return True
            smalls[p] = 1
    return False

def part_one(filename):
    map = get_data(filename)
    return path_count(map)

def part_two(filename):
    map = get_data(filename)
    return alt_count(map)

if __name__ == '__main__':
    print(f"part one test: {part_one('day_12_test')}")
    print(f"part one: {part_one('day_12')}")
    print(f"part two test: {part_two('day_12_test')}")
    print(f"part two: {part_two('day_12')}")