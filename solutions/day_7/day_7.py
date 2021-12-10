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
        positions = [int(x) for x in [d.split(',') for d in data][0]]
    return positions

def part_one(filename):
    positions = get_data(filename)
    target = round(stat.median(positions))
    fuel = 0
    for p in positions:
        fuel += abs(p-target)
    return fuel


def part_two(filename):
    positions = get_data(filename)
    max_pos = max(positions)
    all_values = []
    for x in range(1, max_pos+1):
        fuel = 0
        for p in positions:
            dist = range(1,abs(x-p)+1)
            fuel += sum(dist)
        all_values.append(fuel)
        if fuel > min(all_values):
            return min(all_values)
    return min(all_values)

if __name__ == '__main__':
    count_cache = {}
    print(f"part one test: {part_one('day_7_test')}")
    print(f"part one: {part_one('day_7')}")
    print(f"part two test: {part_two('day_7_test')}")
    print(f"part two: {part_two('day_7')}")