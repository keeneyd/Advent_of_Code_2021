from os import sep
from pathlib import Path
from collections import defaultdict
import math

def relative_path(filename):
    try:
        return f"{Path(__file__).parent.parent.parent}\\data\\{filename}.txt"
    except:
        return f'.\\data\\{filename}.txt'

def string_to_int(c):
    try:
        return int(c)
    except:
        return c

def get_data(filename):
    path = relative_path(filename)
    with open(file=path, mode='r') as data:
        data = data.readlines()
        data = [list(d.replace('\n','').replace(',','')) for d in data]
        for i, dat in enumerate(data):
            for j, d in enumerate(dat):
                data[i][j] = string_to_int(d)
    return data

class snailfish:
    def __init__(self, homework) -> None:
        self.numberlist = [x for x in homework]
        self.number = self.numberlist.pop(0)
        self.magnitude = None

    def add_next(self):
        if len(self.numberlist) > 0:
            self.number.extend(self.numberlist.pop(0))
            self.number.insert(0,'[')
            self.number.insert(-1,']')
        else:
            raise IndexError('No numbers left to add')

    def explode(self):
        parens = 0
        prev_num = None
        current_num = None
        for i, val in enumerate(self.number):
            if val == '[':
                parens += 1
            elif val == ']':
                parens -= 1
            else:
                prev_num = current_num
                current_num = (i,val)
                if parens > 4:
                    if prev_num:
                        self.number[prev_num[0]] += current_num[1]
                    right_num = None
                    next_num = None    
                    for n,value in enumerate(self.number[i+1:]):
                        if type(value) == int and not right_num:
                            right_num = (i+1+n, value )
                            continue
                        if type(value) == int:
                            next_num = ((i+1+n, value ))
                            self.number[next_num[0]] += right_num[1]
                            break
                    self.number[current_num[0]] = 0
                    
                    self.number.pop(right_num[0])
                    self.number.pop(current_num[0]+1)
                    self.number.pop(current_num[0]-1)
                    self.explode()
                    return True
    def split(self):
        for i, val in enumerate(self.number):
            if type(val) != int:
                continue
            if val >= 10:
                self.number.insert(i+1,']')
                self.number.insert(i+1, math.ceil(val/2))
                self.number.insert(i+1, math.floor(val/2))
                self.number.insert(i+1,'[')
                self.number.pop(i)
                self.explode()
                self.split()
                return
    
    def crunch_the_numbers(self):
        while len(self.numberlist) > 0:
            self.add_next()
            self.explode()
            self.split()
            self.magnitude = [n for n in self.number]
        return

    def calc_magnitude(self):
        prev_num = None
        current_num = None
        for i, val in enumerate(self.magnitude):
            if val == '[':
                pass
            elif val == ']' and prev_num:
                new_value = (3 * prev_num[1]) + (2*current_num[1])
                self.magnitude[current_num[0]] = new_value
                self.magnitude.pop(current_num[0]+1)
                self.magnitude.pop(prev_num[0])
                self.magnitude.pop(prev_num[0]-1)
                self.calc_magnitude()
                return
            else:
                prev_num = current_num
                current_num = (i,val)
                
    def __repr__(self) -> str:
        return "".join([str(s) + ',' if type(s) == int else str(s) for s in self.number])

def part_one(filename):
    homework = get_data(filename)
    home = snailfish(homework)
    home.crunch_the_numbers()
    home.calc_magnitude()
    return home.magnitude

def part_two(filename):
    homework = get_data(filename)
    results = []
    for a,val_one in enumerate(homework):
        for b, val_two in enumerate(homework):
            if a != b:
                one = [x for x in val_one]
                two = [x for x in val_two]
                pair = [one,two]
                test= snailfish(pair)
                test.crunch_the_numbers()
                test.calc_magnitude()
                results.append(test.magnitude[0])
    return max(results)

if __name__ == '__main__':
    print(f"part one test: {part_one('day_18_test')}")
    print(f"part one: {part_one('day_18')}")
    print(f"part two test: {part_two('day_18_test')}")
    print(f"part two: {part_two('day_18')}")