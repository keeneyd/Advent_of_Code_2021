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
        data = data.readlines()[0]
        data = data.split(':')[1].strip()
        data = data.replace('x=','').replace('y=','').split()
        data = [d.replace(',','').split('..') for d in data]
    return data

class projectile:

    def __init__(self,target):
        self.target = {}
        self.target['x_min'] = int(target[0][0])
        self.target['x_max'] = int(target[0][1])
        self.target['y_min'] = int(target[1][0])
        self.target['y_max'] = int(target[1][1])
        self.origin = (0,0)
        self.max_height = 0
        self.x_velocity = 0
        self.y_velocity = 0
        self.succesful_velocities = []

    def set_x_velocity(self, velocity):
        self.x_velocity = velocity

    def set_y_velocity(self, velocity):
        self.y_velocity = velocity
    
    def gravity(self):
        self.y_velocity -= 1

    def drag(self):
        if self.x_velocity > 0:
            self.x_velocity -= 1
        if self.x_velocity < 0:
            self.x_velocity += 1

    def fire_projectile(self):
        x,y = self.origin
        xv = self.x_velocity
        yv = self.y_velocity
        max_height =self.max_height
        while x <= self.target['x_max'] and y >= self.target['y_min']:
            print(x,y)
            self.max_height = y if y > self.max_height else self.max_height
            if x >= self.target['x_min'] and y <= self.target['y_max']:
                self.y_velocity = yv
                self.x_velocity = xv
                self.succesful_velocities.append((xv,yv))
                return 'Target Struck'
            x += self.x_velocity
            y += self.y_velocity
            self.drag()
            self.gravity()
        self.y_velocity = yv
        self.x_velocity = xv
        self.max_height = max_height
        return 'Target Missed'

def part_one(filename):
    target = get_data(filename)
    p = projectile(target)

    p.target

    x=0
    x_bottom = 0
    while x < p.target['x_min']:
        x_bottom +=1
        x += x_bottom

    x_bottom  
    x_top = p.target['x_max']+1
    y_bottom = p.target['y_min']
    y_top = abs(y_bottom) + 1
    for x in range(x_bottom,x_top):
        for y in range(y_bottom,y_top):
            p.set_x_velocity(x)
            p.set_y_velocity(y)
            p.fire_projectile()
    return p.max_height, len(p.succesful_velocities)
    
def part_two(filename):
    target = get_data(filename)
    p = projectile(target)

    p.target

    x=0
    x_bottom = 0
    while x < p.target['x_min']:
        x_bottom +=1
        x += x_bottom

    x_bottom  
    x_top = p.target['x_max']+1
    y_bottom = p.target['y_min']
    y_top = abs(y_bottom) + 1
    for x in range(x_bottom,x_top):
        for y in range(y_bottom,y_top):
            p.set_x_velocity(x)
            p.set_y_velocity(y)
            p.fire_projectile()
    p.max_height
    return len(p.succesful_velocities)


if __name__ == '__main__':
    height, count = part_one('day_17_test')
    print(f"part one test: {height}")
    print(f"part two test: {count}")
    height, count = part_one('day_17')
    print(f"part one: {height}")
    print(f"part two: {count}")
   