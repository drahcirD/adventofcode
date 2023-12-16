#! /usr/bin/env python
import operator
import pathlib
from pprint import pprint
import fire
import collections
import itertools
import more_itertools
import numpy as np

from aocd import data as aoc_data
from aocd import submit


def parse(data):
    return {
        (x, y): vy for x, vx in enumerate(data.split("\n")) for y, vy in enumerate(vx)
    }


def handle_movement(pos, direction, data):
    new = set()
    if data[(int(pos.real), int(pos.imag))] == "/":
        if direction == 1j:
            direction = -1
        elif direction == -1j:
            direction = 1
        elif direction == 1:
            direction = -1j
        elif direction == -1:
            direction = 1j

    elif data[(int(pos.real), int(pos.imag))] == "\\":
        if direction == -1j:
            direction = -1
        elif direction == 1j:
            direction = 1
        elif direction == 1:
            direction = 1j
        elif direction == -1:
            direction = -1j
    elif data[(int(pos.real), int(pos.imag))] == "|":
        if direction == 1j:
            new.add((pos, 1))
            direction = -1
        elif direction == -1j:
            new.add((pos, 1))
            direction = -1
    elif data[(int(pos.real), int(pos.imag))] == "-":
        if direction == 1:
            new.add((pos, 1j))
            direction = -1j
        elif direction == -1:
            new.add((pos, 1j))
            direction = -1j

    new.add((pos, direction))
    return new


def p1(data=aoc_data):
    data = parse(data)

    beams = set()
    energized = set([(0 + 0j)])
    pos, direction = (0 + 0j, 1j)

    beams = handle_movement(pos, direction, data)
    states = set()
    while beams:
        states |= beams
        new_beams = set()
        for beam in beams:
            pos, direction = beam
            pos += direction
            if (int(pos.real), int(pos.imag)) not in data:
                continue

            energized.add(pos)
            new_beams |= handle_movement(pos, direction, data)

        beams = new_beams - states

    return len(energized)


def parse2(data):
    return parse(data)


def p2(data=aoc_data):
    data = parse2(data)

    max_x = max(data, key=operator.itemgetter(0))[0]
    max_y = max(data, key=operator.itemgetter(1))[1]
    starts = []

    for i in range(max_x + 1):
        starts.append((i + 0j, 1j))
        starts.append((complex(i, max_y), -1j))
    for i in range(max_y + 1):
        starts.append((complex(0, i), 1))
        starts.append((complex(max_y, i), -1))

    energized = collections.defaultdict(set)
    for start in starts:
        beams = set()
        energized[start] = set([start[0]])
        pos, direction = start
        beams = handle_movement(pos, direction, data)

        states = set()
        while beams:
            states |= beams
            new_beams = set()
            for beam in beams:
                pos, direction = beam
                pos += direction
                if (int(pos.real), int(pos.imag)) not in data:
                    continue

                energized[start].add(pos)

                new_beams |= handle_movement(pos, direction, data)

            beams = new_beams - states
    return max([len(x) for x in energized.values()])


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
