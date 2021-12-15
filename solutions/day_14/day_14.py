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
        rules = [d.replace('\n','') for d in data]
        template = list(rules.pop(0))
        rules = [r.split(' -> ') for r in rules if r != '' ]
        rules = {x:y for x,y in rules}
    return template, rules


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return self.data

class LinkedList:
    def __init__(self, nodes=None):
        self.head = None
        self.element_count = defaultdict(int)
        if nodes is not None:
            node = Node(data=nodes.pop(0))
            self.element_count[node.data] += 1
            self.head = node
            for elem in nodes:
                node.next = Node(data=elem)
                node = node.next
                self.element_count[elem] += 1

    def __repr__(self):
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(node.data)
            node = node.next
        nodes.append("None")
        return " -> ".join(nodes)

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def pair_insertion(self, rules):
        if self.head is None:
            raise Exception("List is empty")
        prev_node = Node(None)
        for node in self:
            if prev_node.data is not None:
                new_data = rules[prev_node.data + prev_node.next.data]
                self.element_count[new_data] += 1
                new_node = Node(new_data)
                new_node.next = node
                prev_node.next = new_node
            prev_node = node            
        return

def part_one(filename):
    template, rules = get_data(filename)
    polymer = LinkedList(template)
    for i in range(0,10):
        polymer.pair_insertion(rules)
    return max(polymer.element_count.values()) - min(polymer.element_count.values())

def part_two(filename):
    template, rules = get_data(filename)
    pair_rules = {}
    for key, value in rules.items():
        pair_rules[key] = [key[0]+value, value+key[1]]

    last_element  = template[-1]

    pair_values = defaultdict(int)
    for i in range(len(template)-1):
        pair = template[i]+template[i+1]
        pair_values[pair] += 1

    for i in range(40):
        new_values = defaultdict(int)
        for key, value in pair_values.items():
            for pair in pair_rules[key]:
                new_values[pair] += value
        pair_values = new_values

    value_counts = defaultdict(int)

    for pair, value in pair_values.items():
        x, y = pair
        value_counts[x] += value    
    
    value_counts[last_element] += 1
    return max(value_counts.values()) - min(value_counts.values())

if __name__ == '__main__':
    print(f"part one test: {part_one('day_14_test')}")
    print(f"part one: {part_one('day_14')}")
    print(f"part two test: {part_two('day_14_test')}")
    print(f"part two: {part_two('day_14')}")