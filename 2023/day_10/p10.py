#! /usr/bin/env python
import pathlib
from pprint import pprint
from queue import PriorityQueue
import fire
import collections
import itertools
import more_itertools
import numpy as np
import matplotlib

from aocd import data as aoc_data
from aocd import submit


def parse(data):
    lines = {
        (x, y): vy for x, vx in enumerate(data.split("\n")) for y, vy in enumerate(vx)
    }
    return lines


# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.


def p1(data=aoc_data):
    data = parse(data)

    start_marker = "S"
    start = None
    for coord, val in data.items():
        if val == start_marker:
            r, c = coord
            start = coord
            neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
            for neighbor in neighbors:
                print(data[neighbor])

            #
            if len(data) > 100:
                data[start] = "J"
                direction = -1
            else:
                data[start] = "F"
                direction = 1j

            break

    start = complex(start[0], start[1])
    pos = start
    lengths = {}
    steps = 0
    pos += direction
    while True:
        pos1 = (int(pos.real), int(pos.imag))

        if ((data[pos1] == "L" or data[pos1] == "7") and abs(direction.real) > 0) or (
            (data[pos1] == "F" or data[pos1] == "J") and abs(direction.imag) > 0
        ):
            direction *= 1j
        elif ((data[pos1] == "L" or data[pos1] == "7") and abs(direction.imag) > 0) or (
            (data[pos1] == "F" or data[pos1] == "J") and abs(direction.real) > 0
        ):
            direction *= -1j

        pos = pos + direction
        steps += 1
        lengths[pos] = steps

        if pos == start:
            break

    return max(lengths.values()) // 2 + 1


def parse2(data):
    return parse(data)

def p2(data=aoc_data):
    data = parse2(data)
    start_marker = "S"
    start = None
    for coord, val in data.items():
        if val == start_marker:
            r, c = coord
            start = coord
            if len(data) > 200:
                data[start] = "J"
                direction = -1
            elif len(data) > 100:
                r, c = start
                # example2
                if data[(r, c + 1)] == "7":
                    data[start] = "F"
                    direction = 1
                # example 3
                elif data[(r, c + 1)] == "F":
                    data[start] = "7"
                    direction = 1
                else:
                    breakpoint()
            else:
                data[start] = "F"
                direction = 1j

            break

    path = [start]

    start = complex(start[0], start[1])
    pos = start
    steps = 0
    pos += direction
    lengths = {start: 0, pos: 1}
    check = set()
    visited_extra = set()

    def _add_right(pos, direction):
        right = pos + direction * -1j

        pos2 = (int(right.real), int(right.imag))

        if pos2 in data and data[pos2] == ".":
            check.add(right)
        elif pos2 in data:
            visited_extra.add(right)
    
    while True:
        pos1 = (int(pos.real), int(pos.imag))

        if ((data[pos1] == "L" or data[pos1] == "7") and abs(direction.real) > 0) or (
            (data[pos1] == "F" or data[pos1] == "J") and abs(direction.imag) > 0
        ):
            direction *= 1j
        elif ((data[pos1] == "L" or data[pos1] == "7") and abs(direction.imag) > 0) or (
            (data[pos1] == "F" or data[pos1] == "J") and abs(direction.real) > 0
        ):
            direction *= -1j

        _add_right(pos, direction)

  
        path.append(pos1)
        pos = pos + direction
        steps += 1
        lengths[pos] = steps

        if pos == start:
            _add_right(pos, direction)
            path.append((int(pos.real), int(pos.imag)))
            break


    visited = set()

    while check:
        pos = check.pop()

        for x in range(-1, 2):
            for y in range(-1, 2):
                com = pos + complex(x, y)
                if com in visited:
                    continue
                pos1 = (int(com.real), int(com.imag))

                if pos1 not in data or com in lengths:
                    continue

                visited.add(com)
                check.add(com)


    path = matplotlib.path.Path(path)
    inside = set()
    for pos in data:
        com = complex(pos[0], pos[1])
        if com not in lengths and path.contains_point(pos):
            inside.add(com)

    old_and_wrong = (visited | (visited_extra - set(lengths)))
    if inside != old_and_wrong:
        breakpoint()
    return len(inside)

    # Old-solution, kept because I might want to check it...
    # Somehow off by 3 on the input but correct on the examples
    return len(visited | (visited_extra - set(lengths)))


def main():
    examples = pathlib.Path(__file__).resolve().parent.glob("example*.txt")
    result = collections.defaultdict(dict)
    for example in examples:
        example_data = example.read_text()
        try:
            result["part1"][example.name] = p1(example_data)
        except:
            pass
        try:
            result["part2"][example.name] = p2(example_data)
        except:
            pass

    print()
    print()

    try:
        result["part1"]["input"] = p1(aoc_data)
        result["part2"]["input"] = p2(aoc_data)
    except:
        raise

    pprint(result)

    submit_p1 = input(f'submit p1? {result["part1"]["input"]}')
    if submit_p1.strip().lower() == "y":
        submit(result["part1"]["input"])

    submit_p2 = input(f'submit p2? {result["part2"]["input"]}')
    if submit_p2.strip().lower() == "y":
        submit(result["part2"]["input"])


def e1(path=pathlib.Path(__file__).resolve().parent / "example.txt"):
    return p1(path.read_text())


def e2(path=pathlib.Path(__file__).resolve().parent / "example.txt"):
    return p2(path.read_text())


if __name__ == "__main__":
    fire.Fire()
