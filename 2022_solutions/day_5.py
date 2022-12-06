from pathlib import Path

def relative_path(filename):
    try:
        return f"{Path(__file__).parent.parent}\\2022_data\\{filename}.txt"
    except:
        return f'.\\2022_data\\{filename}.txt'

def read_data(filename):
    path = relative_path(filename)
    with open(file=path, mode='r') as data:
        raw = [d for d in data]
        _map = raw[:raw.index('\n')]
        _map = [[line[i:i+4].replace('\n','').replace('[','').replace(']','').strip() for i in range(0, len(line) ,4)]for line in _map]
        _dir = [d.split() for d in raw[raw.index('\n')+1:]]
        _dir = [[int(d[1]),int(d[3]),int(d[5])] for d in _dir]
        return _map, _dir

class cargo_stack:
    def __init__(self, _map = []):
        if len(_map)>0:
            self.stacks = [[] for _ in range(len(_map[0]))]
            for m in _map:
                for i, c in enumerate(m):
                    if not c.isnumeric() and c != '':
                        self.stacks[i].append(c)
        else:
            self.stacks = []
        self.map = _map

    def move_crates(self, vol = 0, source = 0, dest = 0):
        moves = vol if vol < len(self.stacks[source]) else len(self.stacks[source])
        for i in range(moves):
            if len(self.stacks[source])>0:
                self.stacks[dest].insert(0,self.stacks[source].pop(0))

    def move_crates_9001(self, vol = 0, source = 0, dest = 0):
        moves = vol if vol < len(self.stacks[source]) else len(self.stacks[source])
        items = self.stacks[source][:moves]
        self.stacks[source] = self.stacks[source][moves:]
        self.stacks[dest] = items + self.stacks[dest]

    def top_crates(self):
        return [c[0] for c in self.stacks if len(c) > 0 ]


def part_one(filename):
    data, directions = read_data(filename)
    cargo = cargo_stack(_map = data)
    cargo.stacks
    for d in directions:
        cargo.move_crates(vol = d[0], source=d[1]-1, dest=d[2]-1)
    return cargo.top_crates()


def part_two(filename):
    data, directions = read_data(filename)
    cargo = cargo_stack(_map = data)
    cargo.stacks
    for d in directions:
        cargo.move_crates_9001(vol = d[0], source=d[1]-1, dest=d[2]-1)
    return cargo.top_crates()

if __name__ == '__main__':
    print(f"part one test: {part_one('day_5_test')}")
    print(f"part one: {part_one('day_5')}")
    print(f"part two test: {part_two('day_5_test')}")
    print(f"part two: {part_two('day_5')}")
