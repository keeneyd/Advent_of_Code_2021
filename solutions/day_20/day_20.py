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
        data = data.readlines()
        algorithm = data.pop(0).replace('\n','')
        image = [d.replace('\n','') for d in data if d != '\n']
    return algorithm, image

class img:
    def __init__(self, pixels, algorithm) -> None:
        self.algorithm = algorithm
        self.pixels = self.pixel_dict(pixels)
        self.x_min = 0
        self.x_max = len(pixels[0]) - 1
        self.y_min = 0
        self.y_max = len(pixels) - 1
        self.frame = '.'

    def pixel_dict(self, pixels):
        img = defaultdict(str)
        for y in range(len(pixels)-1,-1,-1):
            for x, val in enumerate(pixels[y]):
                img[(x,y)] = val
        return img

    def pixel_enhancer(self, pixel):
        key = ''
        _x, _y = pixel
        for y in range(_y-1, _y+2, 1):
            for x in range(_x-1, _x+2, 1):
                char = self.pixels[x,y]
                if char:
                    key += '1' if self.pixels[x,y] == '#' else '0'
                else:
                    key += '1' if self.frame == '#' else '0'
        idx = int(key, 2)
        return self.algorithm[idx]

    def enhance_image(self):
        enhanced_img = defaultdict(str)
        for y in range(self.y_min - 2, self.y_max + 3):
            for x in range(self.x_min - 2, self.x_max + 3):
                    enhanced_img[(x,y)] = self.pixel_enhancer((x,y))
        x_max = 0
        x_min = 0
        y_max = 0
        y_min = 0
        for x, y in enhanced_img:
            x_max = x if x > x_max else x_max
            x_min = x if x < x_min else x_min
            y_max = y if y > y_max else y_max
            y_min = y if y < y_min else y_min
        self.y_min = y_min
        self.y_max = y_max
        self.x_min = x_min
        self.x_max = x_max
        self.pixels = enhanced_img
        frame = '1' if self.frame == '#' else '0'
        self.frame = self.algorithm[int(frame*9,2)]
        
def part_one(filename):
    algorithm, pixels  = get_data(filename)
    image = img(pixels, algorithm)
    image.enhance_image()
    image.enhance_image()
    return sum([1 if p == '#' else 0  for p in image.pixels.values()])

def part_two(filename):
    algorithm, pixels  = get_data(filename)
    image = img(pixels, algorithm)
    for x in range(0,50):
        print(x+1)
        image.enhance_image()
        print(len(image.pixels))
    return sum([1 if p == '#' else 0  for p in image.pixels.values()])

if __name__ == '__main__':
    print(f"part one test: {part_one('day_20_test')}")
    print(f"part one: {part_one('day_20')}")
    print(f"part two test: {part_two('day_20_test')}")
    print(f"part two: {part_two('day_20')}")