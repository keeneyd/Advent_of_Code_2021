from pathlib import Path

def relative_path(filename):
    try:
        return f"{Path(__file__).parent.parent}\\2022_data\\{filename}.txt"
    except:
        return f'.\\2022_data\\{filename}.txt'

def read_data(filename):
    path = relative_path(filename)
    with open(file=path, mode='r') as data:
        raw = [x.replace('\n','').split(',') for x in data]
        return raw

def check_contains(assignment):
    a1 = assignment[0]
    a2 = assignment[1]
    if min(a1) < min(a2):
        return max(a1) >= max(a2)
    if min(a2) < min(a1):
        return max(a2) >= max(a1)
    else:
        return True

def check_overlap(assignment):
    a1 = assignment[0]
    a2 = assignment[1]
    if min(a1) < min(a2):
        return max(a1) >= min(a2)
    if min(a2) < min(a1):
        return max(a2) >= min(a1)
    else:
        return True

def part_one(filename):
    data = read_data(filename)
    pairs = [[i.split('-') for i in item] for item in data]
    assignments = [[[int(e) for e in elf]for elf in p]for p in pairs]
    fully_contains = [check_contains(a) for a in assignments]
    return sum(fully_contains)


def part_two(filename):
    data = read_data(filename)
    pairs = [[i.split('-') for i in item] for item in data]
    assignments = [[[int(e) for e in elf]for elf in p]for p in pairs]
    overlaps = [check_overlap(a) for a in assignments]
    return sum(overlaps)

data = read_data('day_4_test')
data
pairs = [[i.split('-') for i in item] for item in data]
assignments = [[[int(e) for e in elf]for elf in p]for p in pairs]
assignments[0]


if __name__ == '__main__':
    print(f"part one test: {part_one('day_4_test')}")
    print(f"part one: {part_one('day_4')}")
    print(f"part two test: {part_two('day_4_test')}")
    print(f"part two: {part_two('day_4')}")
