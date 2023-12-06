#! /usr/bin/env python
import operator
import pathlib
import fire
import collections
import itertools

def e1(path = pathlib.Path(__file__).resolve().parent / "example.txt"):
    return p1(path)

def se1(path = pathlib.Path(__file__).resolve().parent / "small.txt"):
    return p1(path)

def e2(path = pathlib.Path(__file__).resolve().parent / "example.txt"):
    return p2(path)

def add_north(data, proposals, removals, elf):
    north = (elf[0], elf[1]-1)
    if north not in data and (north[0]-1, north[1]) not in data and (north[0]+1, north[1]) not in data:
        if north not in proposals:
            proposals[north] = elf
            return True
        else:
            removals.add(north)
            return True
    return False
def add_south(data, proposals, removals, elf):
    south = (elf[0], elf[1]+1)
    if south not in data and (south[0]-1, south[1]) not in data and (south[0]+1, south[1]) not in data:
        if south not in proposals:
            proposals[south] = elf
            return True
        else:
            removals.add(south)
            return True
    return False
def add_west(data, proposals, removals, elf):
    west = (elf[0]-1, elf[1])
    if west not in data and (west[0], west[1]-1) not in data and (west[0], west[1]+1) not in data:
        if west not in proposals:
            proposals[west] = elf
            return True
        else:
            removals.add(west)
            return True
    return False
def add_east(data, proposals, removals, elf):
    east = (elf[0]+1, elf[1])
    if east not in data and (east[0], east[1]-1) not in data and (east[0], east[1]+1) not in data:
        if east not in proposals:
            proposals[east] = elf
            return True
        else:
            removals.add(east)
            return True
    return False
def has_neighbours(data, elf):
    directions = [(x,y) for x in range(-1,2) for y in range(-1,2) if not ( x == 0 and y == 0)]

    for direction in directions:
        if (elf[0]+direction[0], elf[1]+direction[1]) in data:
            return True
    return False

def print_room(room):
    for y in range(max(room, key=lambda x: x[1])[1] + 1):
        for x in range(max(room, key=lambda x: x[0])[0] + 1):
            try:
                print(room[(x, y)], end="")
            except:
                print(".", end="")
        print()

def run(data, steps=10):

    i = 0
    while True:
        
        proposals = {}
        removals = set()
        prev_data = data.copy()
        for elf in data:
            if not has_neighbours(data, elf):
                continue
            if i % 4 == 0:
                if add_north(data, proposals, removals, elf):
                    continue
                if add_south(data, proposals, removals, elf):
                    continue
                if add_west(data, proposals, removals, elf):
                    continue
                if add_east(data, proposals, removals, elf):
                    continue
            elif i % 4 == 1:
                if add_south(data, proposals, removals, elf):
                    continue
                if add_west(data, proposals, removals, elf):
                    continue
                if add_east(data, proposals, removals, elf):
                    continue
                if add_north(data, proposals, removals, elf):
                    continue
            elif i % 4 == 2:
                if add_west(data, proposals, removals, elf):
                    continue
                if add_east(data, proposals, removals, elf):
                    continue
                if add_north(data, proposals, removals, elf):
                    continue
                if add_south(data, proposals, removals, elf):
                    continue
            elif i % 4 == 3:
                if add_east(data, proposals, removals, elf):
                    continue
                if add_north(data, proposals, removals, elf):
                    continue
                if add_south(data, proposals, removals, elf):
                    continue
                if add_west(data, proposals, removals, elf):
                    continue
        i+=1
        for proposal, elf in proposals.items():
            if proposal in removals:
                continue
            del data[elf]
            data[proposal] = '#'
        if steps == -1 and data == prev_data:
            return i
        if i == steps:
            break   

    max_x = max(data, key=operator.itemgetter(0))[0]
    max_y = max(data, key=operator.itemgetter(1))[1]
    min_x = min(data, key=operator.itemgetter(0))[0]
    min_y = min(data, key=operator.itemgetter(1))[1]
    count = 0
    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            if (x,y) not in data:
                count +=1
    return count

def p1(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [x for x in path.read_text().split('\n')]
        elves = {}
        for i, row in enumerate(lines):
            for j, col in enumerate(row):
                if col == ".":
                    continue
                elves[(j, i)] = col
        
        return elves
        
    def solve(data):
        return run(data, steps=10)

    return solve(parse())

def p2(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [x for x in path.read_text().split('\n')]
        elves = {}
        for i, row in enumerate(lines):
            for j, col in enumerate(row):
                if col == ".":
                    continue
                elves[(j, i)] = col
        
        return elves
        
    def solve(data):
        return run(data, steps=-1)
    
    return solve(parse())

def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": p1(example), "input": p1()},
        "part2": {"example": p2(example), "input": p2()},
    }


if __name__ == '__main__':
  fire.Fire()
    
    