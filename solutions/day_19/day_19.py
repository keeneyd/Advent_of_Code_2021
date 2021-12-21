from os import sep
from pathlib import Path
from collections import defaultdict
import math

def relative_path(filename):
    try:
        return f"{Path(__file__).parent.parent.parent}\\data\\{filename}.txt"
    except:
        return f'.\\data\\{filename}.txt'

def get_data(filename):
    path = relative_path(filename)
    with open(file=path, mode='r') as data:
        data = [d.replace('\n','') for d in data]
        scanners = {}
        for d in data:
            if d.startswith('---'):
                scanner = d.replace('---','').strip()
                coords = []
            elif d == '':
                scanners[scanner] = coords
            else:
                c = [int(point) for point in d.split(',')]
                coords.append(c)
        scanners[scanner] = coords
    return scanners

class scanner:
    def __init__(self, points) -> None:
        self.points = [(x,y,z) for x,y,z in points]
        self.origin = (0,0,0)
        self.x_rotate = 0
        self.x_invert = False
        self.y_rotate = 0
        self.y_invert = False
        self.z_rotate = 0
        self.z_invert = False

    def reset_origin(self, new_origin):
        _x,_y,_z = new_origin
        shifted_points = []
        for x,y,z in self.points:
            shifted_points.append((x+_x,y+_y,z+_z))
        self.points = shifted_points
        self.origin = new_origin

    def rotate_z(self):
        rotated_points = []
        for x,y,z in self.points:
            rotated_points.append((y,-x, z))
        self.points = rotated_points
        self.z_rotate = 0 if self.z_rotate == 3 else self.z_rotate + 1

    def invert_z(self):
        inverted_points = []
        for x,y,z in self.points:
            inverted_points.append((x,y,-z))
        self.points = inverted_points
        if self.z_invert:
            self.z_invert = False
        else:
            self.z_invert = True

    def rotate_x(self):
        rotated_points = []
        for x,y,z in self.points:
            rotated_points.append((x, -z, y))
        self.points = rotated_points
        self.x_rotate = 0 if self.x_rotate == 3 else self.x_rotate + 1

    def invert_x(self):
        inverted_points = []
        for x,y,z in self.points:
            inverted_points.append((-x,y,z))
        self.points = inverted_points
        if self.x_invert:
            self.x_invert = False
        else:
            self.x_invert = True

    def rotate_y(self):
        rotated_points = []
        for x,y,z in self.points:
                rotated_points.append((z, y, -x))
        self.points = rotated_points
        self.y_rotate = 0 if self.y_rotate == 3 else self.y_rotate + 1

    def invert_y(self):
        inverted_points = []
        for x,y,z in self.points:
            inverted_points.append((x,-y,z))
        self.points = inverted_points
        if self.y_invert:
            self.y_invert = False
        else:
            self.y_invert = True

    def relative_points(self, index=0):
        if index < len(self.points):
            _x, _y, _z = self.points[index]
        return [(x-_x, y-_y, z-_z) for x,y,z in self.points]

def compare_scans(scan1, scan2):
    for i in range(0,len(scan1.points)-11):
        a_rel = scan1.relative_points(i)
        for j in range(0,len(scan2.points)-11):
            a_matches = []
            b_matches = []
            b_rel = scan2.relative_points(j)
            for idx, val in enumerate(a_rel):
                if val in b_rel:
                    a_matches.append(scan1.points[idx])
                    b_matches.append(scan2.points[b_rel.index(val)])
            if len(a_matches) >= 12:
                return a_matches, b_matches
    return [], []

def compare_scanners(scan_a, scan_b):
    for x in [0,1,2,3]:
        scan_b.rotate_x()
        points_a, points_b = compare_scans(scan_a,scan_b)
        if points_a:
            return points_a,points_b
        for y in [0,1,2,3]:
            scan_b.rotate_y()
            points_a, points_b = compare_scans(scan_a,scan_b)
            if points_a:
                return points_a,points_b
            for z in [0,1,2,3]:
                scan_b.rotate_z()
                points_a, points_b = compare_scans(scan_a,scan_b)
                if points_a:
                    return points_a,points_b
    return [],[]

def compare_to_all(base_scan, scan_list):
    for scan in scan_list:
        if scan.origin == (0,0,0) and base_scan is not scan:
                p1,p2 = compare_scanners(base_scan, scan)
                if p1:
                    print("scan matched")
                    offset = point_diff(p1[0],p2[0])
                    scan.reset_origin(offset)
                    compare_to_all(scan, scan_list)



def point_diff(point1, point2):
    #point1 - point2
    a,b,c = point1
    x,y,z = point2
    return (a-x,b-y,c-z)

def point_add(point1, point2):
    a,b,c = point1
    x,y,z = point2
    return (a+x,b+y,c+z)

def manhattan_distance(point1, point2):
    x,y,z = point_diff(point1, point2)
    return(abs(x)+abs(y)+abs(z))



def part_one(filename):
    scanners = get_data(filename)
    scanners = [scanner(x) for x in scanners.values()]
    compare_to_all(scanners[0],scanners[1:])
    beacons = []
    for scan in scanners:
        beacons.extend(scan.points)

    return(len(set(beacons)))


def part_two(filename):
    scanners = get_data(filename)
    scanners = [scanner(x) for x in scanners.values()]
    compare_to_all(scanners[0],scanners[1:])
    dist = []
    for i, scan in enumerate(scanners):
        for second in scanners[i+1:]:
            dist.append(manhattan_distance(scan.origin, second.origin))
    return max(dist)

if __name__ == '__main__':
    print(f"part one test: {part_one('day_19_test')}")
    print(f"part one: {part_one('day_19')}")
    print(f"part two test: {part_two('day_19_test')}")
    print(f"part two: {part_two('day_19')}")