#! /usr/bin/env python
from functools import reduce
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
    lines = {}

    for y, row in enumerate(data.split("\n")):
        for x, v in enumerate(row):
            lines[(x, y)] = v

    return lines


def get_neighbors(p, max_x, max_y):
    for x in range(-1, 2):
        for y in range(-1, 2):
            q = (p[0] + x, p[1] + y)
            if not (-1 < q[0] < max_x) or not (-1 < q[1] < max_y):
                continue
            yield q


def neighbors_symbol(positions, max_x, max_y, data):
    neighbors = set()
    for q in positions:
        for neigh in get_neighbors(q, max_x, max_y):
            neighbors.add(data[neigh])
    neighbors = [n for n in neighbors if n != "." and not n.isdigit()]
    return bool(neighbors)


def p1(data=aoc_data):
    data = parse(data)

    result = []
    max_x = max(p[0] for p in data) + 1
    max_y = max(p[1] for p in data) + 1

    for y in range(0, max_y):
        positions = []
        nbr = ""

        for x in range(0, max_x):
            p = (x, y)
            if data[p].isdigit():
                nbr += data[p]
                positions.append(p)
            else:
                if nbr:
                    nbr = int(nbr)
                    if neighbors_symbol(positions, max_x, max_y, data):
                        result.append(nbr)
                nbr = ""
                positions = []
        if nbr:
            nbr = int(nbr)
            if neighbors_symbol(positions, max_x, max_y, data):
                result.append(nbr)

    return sum(result)


def parse2(data):
    return parse(data)


def p2(data=aoc_data):
    data = parse2(data)
    parts = {}
    max_x = max(p[0] for p in data) + 1
    max_y = max(p[1] for p in data) + 1
    gears = []

    for y in range(0, max_y):
        positions = []
        nbr = ""

        for x in range(0, max_x):
            p = (x, y)
            if data[p].isdigit():
                nbr += data[p]
                positions.append(p)
            else:
                if data[p] == "*":
                    gears.append(p)
                if nbr:
                    nbr = int(nbr)
                    if neighbors_symbol(positions, max_x, max_y, data):
                        for q in positions:
                            parts[q] = nbr
                nbr = ""
                positions = []
        if nbr:
            nbr = int(nbr)
            if neighbors_symbol(positions, max_x, max_y, data):
                for q in positions:
                    parts[q] = nbr

    result = []
    for p in gears:
        touches = set()
        for neigh in get_neighbors(p, max_x, max_y):
            if neigh in parts:
                touches.add(parts[neigh])
        if len(touches) == 2:
            result.append(reduce(operator.mul, touches, 1))

    return sum(result)


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
