from os import sep
from pathlib import Path
from collections import defaultdict

def relative_path(filename):
    try:
        return f"{Path(__file__).parent.parent.parent}\\data\\{filename}.txt"
    except:
        return f'.\\data\\{filename}.txt'

def get_data(filename):
    path = relative_path(filename)
    with open(file=path, mode='r') as data:
        data = [d.replace('\n','').split(' ') for d in data]
        full_list = []
        sub_list = []
        for step in data:
            if step[0]=='inp':
                full_list.append(sub_list)
                sub_list = [step]
            else:
                sub_list.append(step)
        full_list.append(sub_list)
        del full_list[0]
    return full_list

def add(x,y):
    return int(x) + int(y)

def mul(x,y):
    return int(x) * int(y)

def div(x,y):
    return int(int(x)/int(y))

def mod(x,y):
    return int(x)%int(y)

def eql(x,y):
    return 1 if int(x) == int(y)  else 0

def process_step(direction, var_value, modifier):
    if direction == 'inp':
        return modifier
    if direction == 'mul':
        return mul(var_value,modifier)
    if direction == 'add':
        return add(var_value,modifier)
    if direction == 'div':
        return div(var_value, modifier)
    if direction == 'mod':
        return mod(var_value, modifier)
    if direction == 'eql':
        return eql(var_value,modifier)
    raise Exception ('Invalid Direction')

def stately_process_min(states, inputs, directions):
    new_states = defaultdict(int)
    for _z,path in states.items():
        for input_value in inputs:
            z = _z
            w=x=y=0
            for step in directions:
                if len(step) == 2:
                    w = process_step('inp', step[1], input_value)
                else:
                    operation = step[0]
                    target = step[1].lower()
                    modifier = step[2]
                    modifier = eval(modifier)
                    if target == 'w':
                        w = process_step(operation,w,modifier)
                    if target == 'x':
                        x = process_step(operation,x,modifier)
                    if target == 'y':
                        y = process_step(operation,y,modifier)
                    if target == 'z':
                        z = process_step(operation,z,modifier)            
            new_value = (path*10) + input_value
            if new_states[z] == 0:
                new_states[z] = new_value
            else:
                new_states[z] = new_value if new_value < new_states[z] else new_states[z]
    return new_states

def stately_process_max(states, inputs, directions):
    new_states = defaultdict(int)
    for _z,path in states.items():
        for input_value in inputs:
            z = _z
            w=x=y=0
            for step in directions:
                if len(step) == 2:
                    w = process_step('inp', step[1], input_value)
                else:
                    operation = step[0]
                    target = step[1].lower()
                    modifier = step[2]
                    modifier = eval(modifier)
                    if target == 'w':
                        w = process_step(operation,w,modifier)
                    if target == 'x':
                        x = process_step(operation,x,modifier)
                    if target == 'y':
                        y = process_step(operation,y,modifier)
                    if target == 'z':
                        z = process_step(operation,z,modifier)            
            new_value = (path*10) + input_value
            new_states[z] = new_value if new_value > new_states[z] else new_states[z] 
    return new_states


def part_one(filename):
    a = [1,1,1,1,26,1,26,1,26,26,1,26,26,26]
    b = [14,11,12,11,-10,15,-14,10,-4,-3,13,-3,-9,-12]
    inputs = list(range(1,10))
    directions = get_data(filename)
    states = {0:0}
    for i, direction in enumerate(directions):
        if a[i] == 1:
            states = stately_process_max(states=states, inputs = inputs, directions=direction)
        else:
            filtered_states = defaultdict(int)
            for z, path in states.items():
                w = z%26 + b[i]
                if w in range(1,10):
                    p = path*10 + w
                    _z = z // 26
                    filtered_states[_z] = p if p > filtered_states[_z] else filtered_states[_z]
            states = filtered_states
    return states

def part_two(filename):
    a = [1,1,1,1,26,1,26,1,26,26,1,26,26,26]
    b = [14,11,12,11,-10,15,-14,10,-4,-3,13,-3,-9,-12]
    inputs = list(range(1,10))
    directions = get_data(filename)
    states = {0:0}
    for i, direction in enumerate(directions):
        if a[i] == 1:
            states = stately_process_min(states=states, inputs = inputs, directions=direction)
        else:
            filtered_states = defaultdict(int)
            for z, path in states.items():
                w = z%26 + b[i]
                if w in range(1,10):
                    p = path*10 + w
                    _z = z // 26
                    if filtered_states[_z] == 0:
                        filtered_states[_z] = p
                    else:
                        filtered_states[_z] = p if p < filtered_states[_z] else filtered_states[_z]
            states = filtered_states
    return states

if __name__ == '__main__':
    print(f"part one: {part_one('day_24')}")
    print(f"part two: {part_two('day_24')}")



