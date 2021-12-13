from os import sep
from pathlib import Path
import statistics as stat

def relative_path(filename):
    try:
        return f"{Path(__file__).parent.parent.parent}\\data\\{filename}.txt"
    except:
        return f'.\\data\\{filename}.txt'

def get_data(filename):
    path = relative_path(filename)
    with open(file=path, mode='r') as data:
        lines = [d.replace('\n','').split('-') for d in data]
        options = {}
        for key, value in lines:
            existing_value = options.get(key,[])
            existing_value.append(value)
            options[key] = existing_value

            if key != 'start':
                reverse_value = options.get(value,[])
                reverse_value.append(key)
                options[value] = reverse_value
    return options


def find_next(map, path=['start']):
    if path[-1] == 'end':
        return [path]
    try:    
        next_steps = map[path[-1]]
        return [path + [step] for step in next_steps  if step.isupper() or step not in path]
    except KeyError:
        return [path]

def double_small(path):
    smalls = {}
    for p in path:
        if p.islower():
            count = smalls.get(p,0)
            if count > 0:
                return True
            smalls[p] = 1
    return False

def alt_next(map, path=['start']):
    if path[-1] == 'end':
        return [path]
    try:    
        next_steps = map[path[-1]]
        if double_small(path):
            return [path + [step] for step in next_steps  if step.isupper() or step not in path and step != 'start']
        else:
            return [path + [step] for step in next_steps if step != 'start']
    except KeyError:
        return [path]

def part_one(filename):
    map = get_data(filename)
    path_count = 0
    keep_going  = True
    paths = find_next(map = map, path = ['start'])
    while keep_going:
        temp = []
        for path in paths:
            temp.extend(find_next(map = map, path = path))
        paths = temp
        keep_going = path_count != len(paths)
        path_count = len(paths)
    return path_count

def part_two(filename):
    map = get_data(filename)
    path_count = 0
    keep_going  = True
    paths = alt_next(map = map, path = ['start'])
    while keep_going:
        temp = []
        for path in paths:
            temp.extend(alt_next(map = map, path = path))
        paths = temp
        keep_going = path_count != len(paths)
        path_count = len(paths)
    return path_count

if __name__ == '__main__':
    print(f"part one test: {part_one('day_12_test')}")
    print(f"part one: {part_one('day_12')}")
    print(f"part two test: {part_two('day_12_test')}")
    print(f"part two: {part_two('day_12')}")