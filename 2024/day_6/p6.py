#! /usr/bin/env python
import copy
import pathlib
from pprint import pprint
import fire
import collections
import itertools
import more_itertools
import numpy as np

from aocd import data as aoc_data
from aocd import submit
import tqdm


def parse(data):
    lines = {}

    for y, row in enumerate(data.split("\n")):
        for x, v in enumerate(row):
            lines[(x, y)] = v

    return lines


def p1(data=aoc_data):
    data = parse(data)

    result = 0
    pos = None
    direction = None
    for pos, v in data.items():
        if v == "^":
            direction = 0, -1
            break
        elif v == ">":
            direction = 1, 0
            break

        elif v == "<":
            direction = -1, 0
            break

        elif v == "v":
            direction = 0, 1
            break

    visited = set()
    visited.add(pos)
    while pos in data:
        x, y = pos
        newx = x + direction[0]
        newy = y + direction[1]
        nextpos = newx, newy
        if nextpos not in data:
            break
        if data[nextpos] == "#":
            imag = complex(direction[0], direction[1])
            imag *= 1j
            direction = imag.real, imag.imag
            newx = x + direction[0]
            newy = y + direction[1]
            nextpos = newx, newy
        visited.add(nextpos)
        pos = nextpos

    return len(visited)


def parse2(data):
    return parse(data)


def p2(data=aoc_data):
    data = parse2(data)

    result = 0
    startpos = None
    startdirection = None
    for startpos, v in data.items():
        if v == "^":
            startdirection = 0, -1
            break
        elif v == ">":
            startdirection = 1, 0
            break

        elif v == "<":
            startdirection = -1, 0
            break

        elif v == "v":
            startdirection = 0, 1
            break

    visited = set()
    visited.add(startpos)
    pos = startpos
    direction = startdirection
    while startpos in data:
        x, y = pos
        newx = x + direction[0]
        newy = y + direction[1]
        nextpos = newx, newy
        if nextpos not in data:
            break
        if data[nextpos] == "#":
            imag = complex(direction[0], direction[1])
            imag *= 1j
            direction = imag.real, imag.imag
            newx = x + direction[0]
            newy = y + direction[1]
            nextpos = newx, newy
        visited.add(nextpos)
        pos = nextpos

    edges = set()
    max_x = max(pos[0] for pos in data)
    max_y = max(pos[1] for pos in data)
    for pos in data:
        if pos[0] == 0:
            edges.add(pos)
        if pos[1] == 0:
            edges.add(pos)
        if pos[0] == max_x:
            edges.add(pos)
        if pos[1] == max_y:
            edges.add(pos)

    possible_locs = visited | edges
    for looppos in possible_locs:
        if looppos == startpos or data[looppos] == "#":
            continue
        pos = startpos
        direction = startdirection
        visited = set()
        visited.add((pos, direction))
        while pos in data:
            x, y = pos
            newx = x + direction[0]
            newy = y + direction[1]
            nextpos = newx, newy
            if nextpos not in data:
                break
            while data[nextpos] == "#" or nextpos == looppos:
                imag = complex(direction[0], direction[1])
                imag *= 1j
                direction = imag.real, imag.imag
                newx = x + direction[0]
                newy = y + direction[1]
                nextpos = newx, newy
            if (nextpos, direction) in visited:
                result += 1
                break
            visited.add((nextpos, direction))
            pos = nextpos

    return result


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
