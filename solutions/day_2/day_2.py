from pathlib import Path

def relative_path(filename):
    try:
        return f"{Path(__file__).parent.parent.parent}\\data\\{filename}.txt"
    except:
        return f'.\\data\\{filename}.txt'

def part_one(filename):
    path = relative_path(filename)
    with open(file=path, mode='r') as data:
        depths = [int(n) for n in data]


#in rolling 3 depth avg, middle 2 numbers will always be same, so compare depth[i] to depth[i+3]
def part_two(filename):
    path = relative_path(filename)
    with open(file=path, mode='r') as data:
        depths = [int(n) for n in data]


if __name__ == '__main__':
    print(f"part one test: {part_one('day_2_test')}")
    print(f"part one: {part_one('day_2')}")
    print(f"part two test: {part_two('day_2_test')}")
    print(f"part two: {part_two('day_2')}")