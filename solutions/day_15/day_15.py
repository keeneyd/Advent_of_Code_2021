from os import sep
from pathlib import Path
from collections import defaultdict
import heapq

def relative_path(filename):
    try:
        return f"{Path(__file__).parent.parent.parent}\\data\\{filename}.txt"
    except:
        return f'.\\data\\{filename}.txt'

def get_data(filename):
    path = relative_path(filename)
    with open(file=path, mode='r') as data:
        data = data.readlines()
        grid = [d.strip() for d in data]
        length = len(grid)
        width = len(grid[0])
        grid_dict = defaultdict(int)
        for y in range(length):
            for x in range(width):
                grid_dict[(x,y)] = int(grid[y][x])
    return length, width, grid_dict

def expand_grid_right(grid, width, steps = 4):
    new_grid = {}
    for key,value in grid.items():
        new_grid[key] = value
        x,y = key
        for i in range(steps):
            value = 1 if value == 9 else value + 1
            x = x + width
            new_grid[x,y] = value
    return new_grid

def expand_grid_down(grid, length, steps = 4):
    new_grid = {}
    for key,value in grid.items():
        new_grid[key] = value
        x,y = key
        for i in range(steps):
            value = 1 if value == 9 else value + 1
            y = y + length
            new_grid[x,y] = value
    return new_grid

def construct_graph(length, width, grid):
    graph = defaultdict(list)
    for y in range(length):
            for x in range(width):
                edges = []
                if x < width - 1:
                    edge = (x+1,y)
                    distance = grid[edge]
                    edges += [(edge,distance)]
                if x > 0:
                    edge = (x-1,y)
                    distance = grid[edge]
                    edges += [(edge,distance)]
                if y < length -1:
                    edge = (x,y+1)
                    distance = grid[edge]
                    edges += [(edge, distance)]
                if y > 0:
                    edge = (x,y-1)
                    distance = grid[edge]
                    edges += [(edge, distance)]    
                graph[(x,y)] = edges
    return graph

def shortestPath(graph, source, sink):
    queue, visited = [(0, source, [])], set()
    heapq.heapify(queue)
    # traverse graph with BFS
    while queue:
        (cost, node, path) = heapq.heappop(queue)
        # visit the node if it was not visited before
        if node not in visited:
            visited.add(node)
            path = path + [node]
            # hit the sink
            if node == sink:
                return (cost, path)
            # visit neighbours
            for neighbour, c in graph[node]:
                if neighbour not in visited:
                    heapq.heappush(queue, (cost+c, neighbour, path))
    return float("inf")


def part_one(filename):
    length, width, grid = get_data(filename)
    graph = construct_graph(length=length, width=width, grid=grid)
    start = (0,0)
    end = (width-1,length-1)
    dist, path = shortestPath(graph, start, end)
    return length, width, dist, path

def part_two(filename):
    length, width, grid = get_data(filename)
    new = expand_grid_right(grid, width)
    full = expand_grid_down(new, length)
    length = length * 5
    width = width * 5
    start = (0,0)
    end = (width-1,length-1)
    graph = construct_graph(length = length, width = width, grid = full)
    dist, path = shortestPath(graph, start, end)
    return dist

if __name__ == '__main__':
    print(f"part one test: {part_one('day_15_test')}")
    print(f"part one: {part_one('day_15')}")
    print(f"part two test: {part_two('day_15_test')}")
    print(f"part two: {part_two('day_15')}")