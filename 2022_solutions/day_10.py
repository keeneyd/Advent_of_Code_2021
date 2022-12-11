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

def map_cycles(ops):
    cycle_map = {0:1}
    x = 1
    cycle = 0
    for o in ops:
        if o == 'noop':
            cycle +=1
            cycle_map[cycle] = x
        else:
            op, val = o.split(' ')
            cycle += 2
            x += int(val)
            cycle_map[cycle] = x
    for i in range(20,221,20):
        cycle_map.get(i,cycle_map.get(i-1))
    return cycle_map

def output_image(pixels):
    cols = 40
    rows = len(pixels)//cols
    for row in range(0,rows,1):
        line = ''.join([str(pix) for pix in pixels[row*cols:(row+1)*cols]])
        print(line)
    return None
    
def draw_image(cycle_map):
    image = ['.' for p in range(0,241,1)]
    line = 0
    for cycle in range(1,241,1):
        pixel = cycle-1
        x = cycle_map.get(cycle-1,cycle_map.get(cycle-2,1))
        sprite =(x-1,x,x+1)
        if pixel - (line*40) in sprite:
            image[pixel] = '#'
        if cycle > 0 and cycle % 40 == 0:
            line += 1
    return image

def part_one(filename):
    ops = read_data(filename)
    cycle_map = map_cycles(ops)
    signals = [i * cycle_map.get(i-1,cycle_map.get(i-2)) for i in range(20,221,40)]
    return sum(signals)

def part_two(filename):
    ops = read_data(filename)
    cycle_map = map_cycles(ops)
    img = draw_image(cycle_map)
    output_image(img)
    return None


if __name__ == '__main__':
    print(f"part one test: {part_one('day_10_test')}")
    print(f"part one: {part_one('day_10')}")
    print(f"part two test: ")
    part_two('day_10_test')
    print(f"part two: ")
    part_two('day_10')
