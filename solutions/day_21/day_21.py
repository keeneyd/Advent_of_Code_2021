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
        data = [d.replace('\n','').split(': ') for d in data]
        data = [int(d[1]) for d in data]
    return data


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return str(self.data)

class LinkedList:
    def __init__(self, nodes=None):
        self.head = None
        self.element_count = defaultdict(int)
        self.looped = False
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
            nodes.append(str(node.data))
            node = node.next
            if node == self.head:
                nodes.append("None")
                return " -> ".join(nodes)

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next
            if node == self.head:
                break


class Pawn(LinkedList):
    def __init__(self, nodes, starting_position=0, score = 0):
        super().__init__([x for x in nodes])
        self.position = self.head
        self.score = score
        self.loop_list()
        self.set_start(starting_position)

    def set_start(self, starting_position):
        elem = self.head
        if elem.data == starting_position:
            return
        while True:
            elem = elem.next
            if elem.data == starting_position:
                self.head = elem
                return
            if elem == self.head:
                raise ValueError('starting position does not exist')

    def move_pawn(self, spaces):
        for x in range(0,spaces):
            self.head = self.head.next
        self.score += self.head.data

    def loop_list(self):
        if self.looped == True:
            return True
        self.looped = True
        start = self.head
        elem = start.next
        while True:
            if elem.next is not None:
                elem = elem.next
            else:
                elem.next = self.head
                return 

class Deterministic_Dice(LinkedList):
    def __init__(self, nodes):
        super().__init__([x for x in nodes])
        self.roll_count = 0
        self.loop_list()
    
    def loop_list(self):
        if self.looped == True:
            return True
        self.looped = True
        start = self.head
        elem = start.next
        while True:
            if elem.next is not None:
                elem = elem.next
            else:
                elem.next = self.head
                return 

    def roll(self):
        value = self.head
        self.head = self.head.next
        self.roll_count += 1
        return value.data


def play_game(player_1, player_2, dice):
    while True:
        player_1.move_pawn(dice.roll())
        if player_1.score >= 1000:
            print("player 1 wins")
            return player_2.score * (dice.roll_count*3)
        player_2.move_pawn(dice.roll())
        if player_2.score >= 1000:
            print("player 2 wins")
            return player_1.score * (dice.roll_count*3)
    

def outcomes(dice_sides=3):
    outcomes = []
    for i in range(1,dice_sides+1):
        for j in range(1,dice_sides+1):
            for k in range(1,dice_sides+1):
                outcomes.extend([(i+j+k)])
    return Counter(outcomes)


def dirac_game(p1_start: int, p2_start: int, spaces: int = 10, dice_sides: int = 3, target: int = 21 ):
    possible_outcomes = outcomes(dice_sides)
    p1_wins = 0
    p2_wins = 0
    board = [x for x in range(1,spaces+1)]

    states = defaultdict(int)
    states[(p1_start, p2_start, 0, 0)] = 1

    while states:
        new_states = defaultdict(int)
        for (p1_pos, p2_pos, p1_score, p2_score), count in states.items():
            for p1_outcome, p1_occurences in possible_outcomes.items():
                player_1 = Pawn(board, p1_pos, p1_score)
                player_1.move_pawn(p1_outcome)
                if player_1.score >= target:
                    p1_wins += (p1_occurences * count)
                else:
                    for p2_outcome, p2_occurences in possible_outcomes.items():
                        player_2 = Pawn(board, p2_pos, p2_score)
                        player_2.move_pawn(p2_outcome)
                        if player_2.score >= target:
                            p2_wins += (p1_occurences * p2_occurences * count)
                        else:
                            new_states[(player_1.head.data,player_2.head.data,player_1.score,player_2.score)] += (p1_occurences * p2_occurences * count)
        states = new_states
    return p1_wins, p2_wins

def part_one(filename):
    starts  = get_data(filename)
    board = [x for x in range(1,11)]
    dice_values = [6,5,4,3,2,1,0,9,8,7]
    dice = Deterministic_Dice(dice_values)
    player_1 = Pawn(board, starts[0])
    player_2 = Pawn(board, starts[1])
    value = play_game(player_1, player_2, dice)
    return value

def part_two(filename):
    starts  = get_data(filename)
    results = dirac_game(starts[0],starts[1])
    return max(results)

if __name__ == '__main__':
    print(f"part one test: {part_one('day_21_test')}")
    print(f"part one: {part_one('day_21')}")
    print(f"part two test: {part_two('day_21_test')}")
    print(f"part two: {part_two('day_21')}")