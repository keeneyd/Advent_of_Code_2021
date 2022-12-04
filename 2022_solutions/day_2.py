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
        raw = [tuple(x.replace(' ','').replace('\n','')) for x in data]
        return raw

def selected_score(round):
    selection = round[1]
    values = {'X':1,'Y':2,'Z':3}
    return values.get(selection)

def result_score(round):
    values = {('A','X'):3,
                ('A','Y'):6,
                ('A','Z'):0,
                ('B','X'):0,
                ('B','Y'):3,
                ('B','Z'):6,
                ('C','X'):6,
                ('C','Y'):0,
                ('C','Z'):3,}
    return values.get(round)

def round2_score(round):
    values = {'X':1,'Y':2,'Z':3}
    win = {'A':'Y','B':'Z','C':'X'}
    draw = {'A':'X','B':'Y','C':'Z'}
    lose = {'A':'Z','B':'X','C':'Y'}
    result = round[1]
    opponent = round[0]
    if result == 'X':
        score = values.get(lose.get(opponent)) + 0
    if result =='Y':
        score = values.get(draw.get(opponent)) + 3
    if result == 'Z':
        score = values.get(win.get(opponent)) + 6
    return score


def part_one(filename):
    data = read_data(filename)
    results = [selected_score(d)+result_score(d) for d in data]
    return sum(results)

def part_two(filename):
    data = read_data(filename)
    results = [round2_score(d) for d in data] 
    return sum(results)


if __name__ == '__main__':
    print(f"part one test: {part_one('day_2_test')}")
    print(f"part one: {part_one('day_2')}")
    print(f"part two test: {part_two('day_2_test')}")
    print(f"part two: {part_two('day_2')}")
