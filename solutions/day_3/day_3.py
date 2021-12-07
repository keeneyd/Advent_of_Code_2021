from pathlib import Path

def relative_path(filename):
    try:
        return f"{Path(__file__).parent.parent.parent}\\data\\{filename}.txt"
    except:
        return f'.\\data\\{filename}.txt'

def add_lists(l1: list, l2:list) -> list:
    return [int(x)+int(y) for x , y in zip(l1,l2)]

def list_to_string(list):
    return ''.join([str(l) for l in list])

def most_common(l1):
    base = [0]*len(l1[0])
    for bit in l1:
        base = add_lists(base, bit)
    return [1 if x/len(l1) >= 0.5 else 0 for x in base ]

def least_common(l1):
    base = [0]*len(l1[0])
    for bit in l1:
        base = add_lists(base, bit)
    return [0 if x/len(l1) >= 0.5 else 1 for x in base ]

def oxygen(list, idx = 0):
    common = most_common(list)
    result = []
    for i, value in enumerate(list):
        if int(value[idx]) == common[idx]:
            result.append(value)
    if len(result) == 1:
        result_string = list_to_string(result[0])
        return int(result_string, 2)
    else:
        return oxygen(result, idx = idx +1)
        
def co2(list, idx = 0):
    common = least_common(list)
    result = []
    for i, value in enumerate(list):
        if int(value[idx]) == common[idx]:
            result.append(value)
    if len(result) == 1:
        result_string = list_to_string(result[0])
        return int(result_string, 2)
    else:
        return co2(result, idx = idx +1)

def part_one(filename):
    path = relative_path(filename)
    with open(file=path, mode='r') as data:
        diagnostic = [list(line.replace('\n','')) for line in data]
    gamma = most_common(diagnostic)
    epsilon =least_common(diagnostic)
    gamma = ''.join([str(g) for g in gamma])
    epsilon = ''.join([str(e) for e in epsilon])
    return  int(epsilon, 2) * int(gamma, 2)


def part_two(filename):
    path = relative_path(filename)
    with open(file=path, mode='r') as data:
        diagnostic = [list(line.replace('\n','')) for line in data]
    oxygen_value = oxygen(diagnostic)
    co2_value = co2(diagnostic)
    return oxygen_value * co2_value

if __name__ == '__main__':
    print(f"part one test: {part_one('day_3_test')}")
    print(f"part one: {part_one('day_3')}")
    print(f"part two test: {part_two('day_3_test')}")
    print(f"part two: {part_two('day_3')}")