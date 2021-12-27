from os import sep
from pathlib import Path
from collections import defaultdict, Counter


def relative_path(filename):
    try:
        return f"{Path(__file__).parent.parent.parent}\\data\\{filename}.txt"
    except:
        return f'.\\data\\{filename}.txt'

def get_data(filename):
    path = relative_path(filename)
    with open(file=path, mode='r') as data:
        data = [d.replace('\n','').replace('y=','').replace('x=','').replace('z=','').split(',') for d in data]
        result = []
        for x,y,z in data:
            direction = x[:3].strip()
            x = x[3:]
            line = []
            line.append(direction)
            line.append(tuple([int(c) for c in x.split('..')]))
            line.append(tuple([int(c) for c in y.split('..')]))
            line.append(tuple([int(c) for c in z.split('..')]))
            result.append(line)
    return result

def part_one(filename):
    directions = get_data(filename)
    reactor = defaultdict(str)
    for d, x, y, z in directions:
        for _x in range(min(x),max(x)+1):
            if _x < -50 or _x > 50:
                pass
            else:
                for _y in range(min(y),max(y)+1):
                    if _y < -50 or _y > 50:
                        pass
                    else:
                        for _z in range(min(z),max(z)+1):
                            if _z < -50 or _z > 50:
                                pass
                            else:
                                reactor[(_x,_y,_z)] = d
    return sum([1 if x == 'on' else 0 for x in reactor.values()])

def test_overlap(core_cube,new_cube):
    cx, cy, cz = core_cube
    nx, ny, nz = new_cube
    if min(nx) > max(cx) or max(nx) < min(cx):
        return False
    if min(ny) > max(cy) or max(ny) < min(cy):
        return False
    if min(nz) > max(cz) or max(nz) < min(cz):
        return False
    return True

def cube_count(cube):
    _x, _y, _z = cube
    x_len = abs(_x[0]-_x[1]) + 1
    y_len = abs(_y[0]-_y[1]) + 1
    z_len = abs(_z[0]-_z[1]) + 1
    return (x_len * y_len * z_len)

def split_coordinates(core, new):
    core_high = max(core)
    core_low = min(core)
    new_high = max(new)
    new_low = min(new)
    results = []
    if core_low == new_low and core_high == new_high:
        return [core]
    if core_low == new_low and core_high > new_high:
        results.append((core_low,new_high))
        results.append((new_high+1,core_high))
    if core_low == new_low and core_high < new_high:
        return [core]
    if core_low < new_low and core_high == new_high:
        results.append((core_low,new_low-1))
        results.append((new_low,core_high))
    if core_low < new_low and core_high < new_high:
        results.append((core_low, new_low -1))
        results.append((new_low,core_high))
    if core_low < new_low and core_high > new_high:
        results.append((core_low,new_low-1))
        results.append((new_low,new_high))
        results.append((new_high+1,core_high))
    if core_low > new_low and core_high == new_high:
        return [core]
    if core_low > new_low and core_high < new_high:
        return [core]
    if core_low > new_low and core_high > new_high:
        results.append((core_low,new_high))
        results.append((new_high+1,core_high))
    return results

def split_cube(core_cube, new_cube):
    corex, corey, corez = core_cube
    newx, newy, newz = new_cube
    x_split = split_coordinates(corex, newx)
    y_split = split_coordinates(corey, newy)
    z_split = split_coordinates(corez, newz)
    combos = combine_coordinates(x_split, y_split, z_split)
    return combos

def combine_coordinates(x,y,z):
    combinations = []
    for _x in x:
        for _y in y:
            for _z in z:
                combinations.append([_x,_y,_z])
    return combinations

def contained_in(core_cube,new_cube):
    cx, cy, cz = core_cube
    nx, ny, nz = new_cube
    if max(cx) > max(nx) or min(cx) < min(nx):
        return False
    if max(cy) > max(ny) or min(cy) < min(ny):
        return False
    if max(cz) > max(nz) or min(cz) < min(nz):
        return False    
    return True

def part_two(filename):
    directions = get_data(filename)
    core_cuboid = []
    core_cuboid.append(directions[0][1:])
    for d, newx, newy, newz in directions[1:]:
        new_cube = [newx,newy,newz]
        new_core = []
        for corex, corey, corez in core_cuboid:
            if contained_in([corex, corey, corez],new_cube):
                continue
            if test_overlap([corex, corey, corez],new_cube):
                x_split = split_coordinates(corex, newx)
                y_split = split_coordinates(corey, newy)
                z_split = split_coordinates(corez, newz)

                combos = combine_coordinates(x_split, y_split, z_split)
                for sub_cube in combos:
                    if not contained_in(sub_cube, new_cube):
                        new_core.append(sub_cube)
            else:
                new_core.append([corex, corey, corez])
        if d == 'on':
            new_core.append(new_cube)
        core_cuboid = new_core
    return sum([cube_count(x) for x in core_cuboid])

if __name__ == '__main__':
    print(f"part one test: {part_one('day_22_test')}")
    print(f"part one: {part_one('day_22')}")
    print(f"part two test: {part_two('day_22_test')}")
    print(f"part two: {part_two('day_22')}")