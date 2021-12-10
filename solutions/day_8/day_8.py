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
        lines = [d for d in data]
        lines = [l.split(' | ') for l in lines]
        signal = []
        output = []
        for s, o in lines:
            signal.append([set(sig) for sig in s.split(' ')])
            output.append(o.replace('\n','').split(' '))
    return signal, output

def part_one(filename):
    signal, output = get_data(filename)
    count = 0
    for entry in output:
        for display in entry:
            if len(display) in [2,3,4,7]:
                count += 1
    return count


def signal_decoder(signal):
    sig_length = {}
    sig_map = {}
    for sig in signal:
        key = len(sig)
        val = sig_length.get(key, list())
        val.append(sig)
        sig_length[key] = val
    sig_map[1] = sig_length[2][0]
    sig_map[4] = sig_length[4][0]
    sig_map[7] = sig_length[3][0]
    sig_map[8] = sig_length[7][0]
    for s in sig_length[6]:
        if len(s.union(sig_map[1])) == 7:
            sig_map[6] = s
        elif len(s.union(sig_map[4])) == 6:
            sig_map[9] = s
        else:
            sig_map[0] = s
    for s in sig_length[5]:
        if len(s.union(sig_map[1])) == 5:
            sig_map[3] = s
        if len(s.union(sig_map[4])) == 7:
            sig_map[2] = s
        if len(s.union(sig_map[6])) == 6:
            sig_map[5] = s
    return {frozenset(val):key for (key, val) in sig_map.items()}

def part_two(filename):
    signal, output = get_data(filename)
    sum = 0
    for i, sig in enumerate(signal):
        translator = signal_decoder(sig)
        num = ''
        for digit in output[i]:
            num += str(translator[frozenset(digit)])
        sum += int(num)
    return sum

if __name__ == '__main__':
    print(f"part one test: {part_one('day_8_test')}")
    print(f"part one: {part_one('day_8')}")
    print(f"part two test: {part_two('day_8_test')}")
    print(f"part two: {part_two('day_8')}")
