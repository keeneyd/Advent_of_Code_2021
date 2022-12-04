from pathlib import Path

def relative_path(filename):
    try:
        return f"{Path(__file__).parent.parent}\\2022_data\\{filename}.txt"
    except:
        return f'.\\2022_data\\{filename}.txt'

def read_data(filename):
    path = relative_path(filename)
    increases = 0
    with open(file=path, mode='r') as data:
        raw = data.readlines()
        elf = []
        final = []
        for i in raw:
            try:
                elf.append(int(i))
            except:
                final.append(elf)
                elf = []
        final.append(elf)
        return final

def part_one(filename):
    data = read_data(filename)
    sums = [sum(x) for x in data]
    return max(sums)

def part_two(filename):
    data = read_data(filename)
    sums = [sum(x) for x in data]
    sums.sort(reverse=True)
    return sum(sums[:3])


if __name__ == '__main__':
    print(f"part one test: {part_one('day_1_test')}")
    print(f"part one: {part_one('day_1')}")
    print(f"part two test: {part_two('day_1_test')}")
    print(f"part two: {part_two('day_1')}")
