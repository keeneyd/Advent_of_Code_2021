from pathlib import Path

def relative_path(filename):
    try:
        return f"{Path(__file__).parent.parent.parent}\\data\\{filename}.txt"
    except:
        return f'.\\data\\{filename}.txt'

def part_one(filename):
    path = relative_path(filename)
    x = 0
    y = 0
    with open(file=path, mode='r') as data:
        directions = [line.split(sep=' ') for line in data]
    for dir, val in directions:
        if dir == 'forward':
            x += int(val)
        if dir == 'down':
            y += int(val)
        if dir == 'up':
            y -= int(val)
    return x * y

#in rolling 3 depth avg, middle 2 numbers will always be same, so compare depth[i] to depth[i+3]
def part_two(filename):
    path = relative_path(filename)
    x = 0
    y = 0
    aim = 0
    with open(file=path, mode='r') as data:
        directions = [line.split(sep=' ') for line in data]
    for dir, val in directions:
        if dir == 'forward':
            x += int(val)
            y += (int(val)*aim)
        if dir == 'down':
            aim += int(val)
        if dir == 'up':
            aim -= int(val)
    return x * y

if __name__ == '__main__':
    print(f"part one test: {part_one('day_2_test')}")
    print(f"part one: {part_one('day_2')}")
    print(f"part two test: {part_two('day_2_test')}")
    print(f"part two: {part_two('day_2')}")