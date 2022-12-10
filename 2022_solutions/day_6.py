from pathlib import Path
from collections import Counter

def relative_path(filename):
    try:
        return f"{Path(__file__).parent.parent}\\2022_data\\{filename}.txt"
    except:
        return f'.\\2022_data\\{filename}.txt'

def read_data(filename):
    path = relative_path(filename)
    with open(file=path, mode='r') as data:
        raw = [d for d in data]
        return raw[0]

def find_marker(ds:str, packet_len:int = 4)->int:
    for i in range(len(ds)-(packet_len-1)):
        sub = ds[i:i+packet_len]
        if(max(Counter(sub).values())) == 1:
            return i+packet_len
    return None


def part_one(filename):
    datastream = read_data(filename)
    marker = find_marker(datastream)
    return marker


def part_two(filename):
    datastream = read_data(filename)
    marker = find_marker(datastream, 14)
    return marker

if __name__ == '__main__':
    print(f"part one test: {part_one('day_6_test')}")
    print(f"part one: {part_one('day_6')}")
    print(f"part two test: {part_two('day_6_test')}")
    print(f"part two: {part_two('day_6')}")
