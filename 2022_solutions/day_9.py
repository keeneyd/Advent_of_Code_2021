from pathlib import Path
from collections import defaultdict

def relative_path(filename):
    try:
        return f"{Path(__file__).parent.parent}\\2022_data\\{filename}.txt"
    except:
        return f'.\\2022_data\\{filename}.txt'

def read_data(filename):
    path = relative_path(filename)
    with open(file=path, mode='r') as data:
        raw = [d.replace('\n','') for d in data]
    return raw

def is_adjacent(head, tail):
    hx,hy = head
    tx,ty = tail
    _x = max(hx,tx) - min(hx,tx)
    _y = max(hy,ty) - min(hy,ty)
    return  max(_x,_y) in (0,1)

def first_step(head, tail, map):
    hx,hy = head
    tx,ty = tail
    _x = max(hx,tx) - min(hx,tx)
    _y = max(hy,ty) - min(hy,ty)
    if is_adjacent(head,tail):
        step = tail
    elif _x == 1:
        if hy -ty > 0:
            step = (hx,ty+1)
        else:
            step = (hx,ty-1)
    elif _y == 1:
        if hx - tx > 0:
            step = (tx+1,hy)
        else:
            step = (tx-1,hy)
    else:
        step = tail
    map[step] = 1    
    return  (step, map)

def log_step(map, loc):
    map[loc] = 1
    return map

def catch_up(head,tail,map):
    hx,hy = head
    tx,ty = tail
    step = tail
    if is_adjacent(head,tail):
        step = tail
    elif hx == tx:
        if hy > ty:
            for _y in range(ty,hy,1):
                log_step(map,(tx,_y))
                step = (tx,_y)
        if hy < ty:
            for _y in range(ty,hy,-1):
                log_step(map,(tx,_y))
                step = (tx,_y)
    elif hy == ty:
        if hx>tx:
            for _x in range(tx,hx,1):
                log_step(map,(_x,ty))
                step = (_x,ty)
        if hx < tx:
            for _x in range(tx,hx,-1):
                log_step(map,(_x,ty))
                step = (_x,ty)
    return (step,map)

def move_head(d, head):
    dir, val = d.split(' ')
    x,y = head
    if dir == 'R':
        x+=int(val)
    if dir == 'L':
        x-=int(val)
    if dir == 'U':
        y+=int(val)
    if dir == 'D':
        y-=int(val)
    return (x,y)

def step_piece(d, head):
    x,y = head
    if d == 'R':
        x+=1
    if d == 'L':
        x-=1
    if d == 'U':
        y+=1
    if d == 'D':
        y-=1
    return (x,y)

def single_step(head, tail, map):
    hx,hy = head
    tx,ty = tail
    if is_adjacent(head,tail):
        step = tail
    else:
        if hx > tx:
            tx += 1
        elif hx < tx:
            tx -= 1
        if hy > ty:
            ty += 1
        elif hy < ty:
            ty -= 1
        step = (tx,ty)
    map[step] = 1    
    return  (step, map)

def part_one(filename):
    directions = read_data(filename)
    head, tail = ((0,0),(0,0))
    tail_map = dict()
    tail_map = log_step(tail_map,tail)
    for d in directions:
        head = move_head(d,head)
        tail, tail_map = first_step(head,tail,tail_map)
        tail, tail_map = catch_up(head,tail,tail_map)
    return sum(tail_map.values())

def part_two(filename):
    directions = read_data(filename)
    rope = [(0,0) for i in range(0,10)]
    tail_map = dict()
    for d in directions:
        dir, val = d.split(' ')
        for v in range(0,int(val)):
            for i,knot in enumerate(rope):
                if i == 0:
                    rope[i] = step_piece(dir,knot)
                elif i != 9:
                    h = rope[i-1]
                    t = knot
                    t, _map = single_step(h,t,dict())
                    rope[i] = t
                else:
                    h = rope[i-1]
                    t = knot
                    t, tail_map = single_step(h,t,tail_map)
                    rope[i] = t
    return sum(tail_map.values())

if __name__ == '__main__':
    print(f"part one test: {part_one('day_9_test')}")
    print(f"part one: {part_one('day_9')}")
    print(f"part two test: {part_two('day_9_test')}")
    print(f"part two: {part_two('day_9')}")
