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
    return data

class Bitstream:
    def __init__(self, hexstream):
        self.hex_to_binary, self.binary_to_hex = self.hex_translator()
        self.bitstream = self.hex_string_to_bit_string(hexstream)
        # number of bits read overall
        self.read = 0
        # sum of all versions
        self.versionsum = 0

    def hex_translator(self):
        decoder = """
        0 = 0000
        1 = 0001
        2 = 0010
        3 = 0011
        4 = 0100
        5 = 0101
        6 = 0110
        7 = 0111
        8 = 1000
        9 = 1001
        A = 1010
        B = 1011
        C = 1100
        D = 1101
        E = 1110
        F = 1111"""
        decoder = [d.strip().split(' = ') for d in decoder.split('\n') if d != '']
        hex_to_binary = {}
        binary_to_hex = {}
        for key,value in decoder:
            hex_to_binary[key] = value
            binary_to_hex[value] = key
        return hex_to_binary, binary_to_hex

    def hex_string_to_bit_string(self, hex_string):
        bit_string = ''
        for char in hex_string:
            bit_string += self.hex_to_binary[char]
        return bit_string

    def get_bits(self, n):
        start = self.read
        self.read += n
        bits = self.bitstream[start:self.read]
        return bits

    def decode_bits(self, x):
        return int("".join([str(b) for b in x]), 2)

    def get_literal(self):
        number = []
        while True:
            last = self.decode_bits(self.get_bits(1)) == 0
            number.extend(self.get_bits(4))
            if last:
                break
        return self.decode_bits(number)

    def version_sum(self):
        version = self.decode_bits(self.get_bits(3))
        id = self.decode_bits(self.get_bits(3))
        self.versionsum += version

        if id == 4: # literal packet
            self.get_literal()
        else: # operator packet
            lengthtype = self.decode_bits(self.get_bits(1))
            if lengthtype == 0: # bit length
                length = self.decode_bits(self.get_bits(15))
                pos = self.read
                while pos + length > self.read:
                    self.decode_packet()
            elif lengthtype == 1: # number of subpackets
                subpackets = self.decode_bits(self.get_bits(11))
                for _ in range(subpackets):
                    self.decode_packet()

    def decode_packet(self):
        version = self.decode_bits(self.get_bits(3))
        id = self.decode_bits(self.get_bits(3))
        self.versionsum += version

        if id == 4: # literal packet
            value = self.get_literal()
        else: # operator packet
            lengthtype = self.decode_bits(self.get_bits(1))
            v = [] # collect all literals
            if lengthtype == 0: # bit length
                length = self.decode_bits(self.get_bits(15))
                pos = self.read
                while pos + length > self.read:
                    v.append(self.decode_packet())
            elif lengthtype == 1: # number of subpackets
                subpackets = self.decode_bits(self.get_bits(11))
                for _ in range(subpackets):
                    v.append(self.decode_packet())
            else:
                raise ValueError(f"Unknown lengthtype: {lengthtype}")
        
            if id == 0: # +
                value = sum(v)
            elif id == 1: # *
                value = v[0]
                for num in v[1:]:
                    value *= num
            elif id == 2: # min
                value = min(v)
            elif id == 3: # max
                value = max(v)
            elif id == 5: # >
                value = int(v[0] > v[1])
            elif id == 6: # <
                value = int(v[0] < v[1])
            elif id == 7: # ==
                value = int(v[0] == v[1])
            else:
                raise ValueError(f"Unknown operator: {id}")
        return value

def part_one(filename):
    hex = get_data(filename)
    bit = Bitstream(hex)
    bit.version_sum()
    return bit.versionsum

def part_two(filename):
    hex = get_data(filename)
    bit = Bitstream(hex)
    value = bit.decode_packet()
    return value

if __name__ == '__main__':
    print(f"part one test: {part_one('day_16_test')}")
    print(f"part one: {part_one('day_16')}")
    print(f"part two test: {part_two('day_16_test')}")
    print(f"part two: {part_two('day_16')}")

