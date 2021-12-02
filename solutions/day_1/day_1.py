from pathlib import Path

def relative_path(filename):
    try:
        return f"{Path(__file__).parent.parent.parent}\\data\\{filename}.txt"
    except:
        return f'.\\data\\{filename}.txt'

def part_one(filename):
    path = relative_path(filename)
    increases = 0
    with open(file=path, mode='r') as data:
        depths = [int(n) for n in data]
    for i,depth in enumerate(depths):
        if i == len(depths)-1:
            return increases
        if depth < depths[i+1]:
            increases += 1

#in rolling 3 depth avg, middle 2 numbers will always be same, so compare depth[i] to depth[i+3]
def part_two(filename):
    path = relative_path(filename)
    increases = 0
    with open(file=path, mode='r') as data:
        depths = [int(n) for n in data]
    for i,depth in enumerate(depths):
        if i == len(depths)-3:
            return increases
        if depth < depths[i+3]:
            increases += 1

if __name__ == '__main__':
    print(f"part one test: {part_one('day_1_test')}")
    print(f"part one: {part_one('day_1')}")
    print(f"part two test: {part_two('day_1_test')}")
    print(f"part two: {part_two('day_1')}")