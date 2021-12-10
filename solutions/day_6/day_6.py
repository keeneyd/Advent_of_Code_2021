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
        lanternfish = [d.split(',') for d in data][0]
        lanternfish = [int(fish) for fish in lanternfish]
    return lanternfish

def growth_map(days = 100):
    fish = [6]
    count = [len(fish)]
    for d in range(0,days):
        for i, f in enumerate(fish):
            if f == 0:
                fish[i] = 6
                fish.append(9)
            else:
                fish[i] = f-1
        count.append(len(fish))
        print(f'day {d} : {count[-1]}')
    return count

def part_one(filename):
    fish = get_data(filename)
    pop_count = growth_map()
    total_pop = 0
    for f in fish:
        i = 80 + (6-f)
        total_pop += pop_count[i]
    return total_pop

def ancestor_count(age, days):
    count = 1
    try:
        count = count_cache[(age,days)]
    except:
        for p in range(age+1, days+1, 7):   
            count += ancestor_count(8, days-p)
        count_cache[(age,days)] = count
    return count

def part_two(filename):
    days = 256
    fish = get_data(filename)
    total_pop = 0
    for f in fish:
        total_pop += ancestor_count(f, days)
    return total_pop

if __name__ == '__main__':
    count_cache = {}
    print(f"part one test: {part_one('day_6_test')}")
    print(f"part one: {part_one('day_6')}")
    print(f"part two test: {part_two('day_6_test')}")
    print(f"part two: {part_two('day_6')}")