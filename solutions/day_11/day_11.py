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
        lines = [list(d.replace('\n','')) for d in data]
        lines = [[int(x) for x in line] for line in lines]
    return lines

class energy_grid:
    def __init__(self, grid_list) -> None:
        self.length = len(grid_list)
        self.width = len(grid_list[0])
        self.grid = self.construct_grid(grid_list)

    def construct_grid(self, grid_list):
        grid = {}
        for i, row in enumerate(grid_list):
            y = self.length - i -1
            for x, cell in enumerate(row):
                grid[(x,y)] = cell
        return grid

    def grid_step(self):
        for key, value in self.grid.items():
            self.grid[key] = value + 1
        return None

    def flash_all(self):
        count = 0
        for key, value in self.grid.items():
            if value >= 10:
                count += self.flash(key)
        return count

    def flash(self, coord):
        x,y = coord
        flash_count = 1
        self.grid[(x,y)] = 0
        for _x in [x-1,x,x+1]:
            for _y in [y-1,y,y+1]:
                if self.grid.get((_x,_y),0) != 0:
                    self.grid[_x,_y] += 1
                    if self.grid[_x,_y] > 9:
                        flash_count += self.flash((_x,_y))
        return flash_count

    def synchronize_flashes(self):
        step_count = 0
        while sum(self.grid.values()) > 0:
            self.grid_step()
            self.flash_all()
            step_count += 1
        return step_count

    def __repr__(self) -> str:
        output = ''
        for y in range(self.length, 0, -1):
            for x in range(0,self.width, 1):
                output += str(self.grid[(x,y-1)])
                output += ' '
            output += "\n"
        return output

def part_one(filename, steps = 100):
    lines = get_data(filename)
    power_grid = energy_grid(lines)
    flashes = 0
    for i in range(0,steps,1):
        power_grid.grid_step()
        flashes += power_grid.flash_all()
    return flashes

def part_two(filename):
    lines = get_data(filename)
    power_grid = energy_grid(lines)
    steps = power_grid.synchronize_flashes()
    return steps

if __name__ == '__main__':
    print(f"part one test: {part_one('day_11_test')}")
    print(f"part one: {part_one('day_11')}")
    print(f"part two test: {part_two('day_11_test')}")
    print(f"part two: {part_two('day_11')}")