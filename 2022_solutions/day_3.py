from pathlib import Path
import string

def relative_path(filename):
    try:
        return f"{Path(__file__).parent.parent}\\2022_data\\{filename}.txt"
    except:
        return f'.\\2022_data\\{filename}.txt'

def read_data(filename):
    path = relative_path(filename)
    increases = 0
    with open(file=path, mode='r') as data:
        raw = [(x.replace('\n','')) for x in data]
        return raw

def priority_dict():
    priority = {}
    for i,letter in enumerate(string.ascii_lowercase,1):
        priority[letter]=i
    for i, letter in enumerate(string.ascii_uppercase,27):
        priority[letter] = i
    return priority

def compartmentalize(contents):
    middle = len(contents)//2
    return [set(contents[:middle]),set(contents[middle:])]

def part_one(filename):
    data = read_data(filename)
    p = priority_dict()
    compartmentalized = [compartmentalize(d) for d in data]
    overlap = [list(c[0].intersection(c[1])) for c in compartmentalized]
    priorities = [sum([p.get(i) for i in x]) for x in overlap]
    return sum(priorities)


def part_two(filename):
    p = priority_dict()
    data = read_data(filename)
    data_sets = [set(d) for d in data]
    grouped = [data_sets[i:i+3] for i in range(0,len(data_sets),3)]
    badges = [list(set.intersection(*g)) for g in grouped]
    priorities = [sum([p.get(i) for i in x]) for x in badges]
    return sum(priorities)


if __name__ == '__main__':
    print(f"part one test: {part_one('day_3_test')}")
    print(f"part one: {part_one('day_3')}")
    print(f"part two test: {part_two('day_3_test')}")
    print(f"part two: {part_two('day_3')}")
