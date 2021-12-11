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
        pairs = {'(':')', '[':']', '{':'}', '<':'>'}
        corrupt_scores = {')':3, ']':57, '}':1197, '>':25137}
        inc_scores = {'(':1, '[':2, '{':3, '<':4}
        lines = [list(d.replace('\n','')) for d in data]
    return pairs, corrupt_scores, inc_scores, lines

def check_line(line, pairs):
    tracker = []
    for l in line:
        if l in pairs.keys():
            tracker += l
        if l in pairs.values():
            if l != pairs[tracker.pop(-1)]:
                return l
    return ''

def check_complete(line, pairs):
    tracker = []
    for l in line:
        if l in pairs.keys():
            tracker += l
        if l in pairs.values():
            if l != pairs[tracker.pop(-1)]:
                return None
    return tracker

def corrupt_score(characters: list, scorecard: dict) -> int:
    sum = 0
    for c in characters:
        sum += scorecard[c]
    return sum

def incomplete_score(characters: list, scorecard: dict) -> int:
    score = 0
    for c in reversed(characters):
        score *= 5
        score += scorecard[c]
    return score
        

def part_one(filename):
    pairs, scores, x, lines = get_data(filename)
    corrupt = []
    for line in lines:
        corrupt += check_line(line, pairs)
    score = corrupt_score(corrupt, scores)
    return score

def part_two(filename):
    pairs, x, scores, lines = get_data(filename)
    incomplete = []
    for line in lines:
        if check_complete(line, pairs):
            incomplete.append(check_complete(line, pairs))
    score = []
    for inc in incomplete:
        score.append(incomplete_score(inc, scores))
    return stat.median(score)

if __name__ == '__main__':
    print(f"part one test: {part_one('day_10_test')}")
    print(f"part one: {part_one('day_10')}")
    print(f"part two test: {part_two('day_10_test')}")
    print(f"part two: {part_two('day_10')}")