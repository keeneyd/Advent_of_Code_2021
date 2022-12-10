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

def parse_directory(directions:list)->defaultdict:
    directory = defaultdict(list)
    path = []
    for d in directions:
        if d.startswith('$ cd'):
            if d == '$ cd ..':
                path.pop(-1)
            else:
                current_dir = d.replace('$ cd ','')
                path.append(current_dir)
            continue
        if d.startswith('$ ls'):
            continue
        directory[tuple(path)].append(d)
    return directory

def size_folder(directory:defaultdict, folder:tuple):
    folder_contents = directory[folder]
    folder_size = 0
    for item in folder_contents:
        if item.startswith('dir'):
            next = item.replace('dir ','')
            sub_folder = folder + (next,)
            folder_size += size_folder(directory, sub_folder)
        else:
            file_size = int(item.split(' ')[0])
            folder_size += file_size
    return folder_size

def part_one(filename):
    directions = read_data(filename)
    directory = parse_directory(directions)
    folders = dict()
    for folder in directory:
        folders[folder] = size_folder(directory, folder)
    candidates = [x for x in folders.values() if x <= 100000]
    return sum(candidates)

def part_two(filename):
    directions = read_data(filename)
    directory = parse_directory(directions)
    folders = dict()
    for folder in directory:
        folders[folder] = size_folder(directory, folder) 
    total_space = 70000000
    needed_space = 30000000
    used_space = folders[('/',)]
    unused_space = total_space - used_space
    delta = needed_space - unused_space
    candidates = [x for x in folders.values() if x >= delta]
    return min(candidates)


if __name__ == '__main__':
    print(f"part one test: {part_one('day_7_test')}")
    print(f"part one: {part_one('day_7')}")
    print(f"part two test: {part_two('day_7_test')}")
    print(f"part two: {part_two('day_7')}")
