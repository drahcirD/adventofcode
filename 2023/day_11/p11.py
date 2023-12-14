#! /usr/bin/env python
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
    lines = {
        (x, y): vy for x, vx in enumerate(data.split("\n")) for y, vy in enumerate(vx)
    }
    col_with_galaxies = set()
    rows_with_galaxies = set()
    galaxies = {}
    n = 1
    for y in range(max(lines, key=lambda x: x[1])[1] + 1):
        for x in range(max(lines, key=lambda x: x[0])[0] + 1):
            if lines[(x, y)] == "#":
                galaxies[(x, y)] = n
                n += 1
                col_with_galaxies.add(y)
                rows_with_galaxies.add(x)

    rows_without_galaxies = (
        set(range(max(lines, key=lambda x: x[0])[0] + 1)) - rows_with_galaxies
    )
    cols_without_galaxies = (
        set(range(max(lines, key=lambda x: x[1])[1] + 1)) - col_with_galaxies
    )

    galaxy_map = {}
    for pos, galaxy in galaxies.items():
        x, y = pos
        x += len([row for row in rows_without_galaxies if row < x])
        y += len([col for col in cols_without_galaxies if col < y])
        galaxy_map[(x, y)] = galaxy

    return galaxy_map


def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def p1(data=aoc_data):
    data = parse(data)

    result = 0
    mins = dict()
    done = set()
    for pos, galaxy in data.items():
        for pos2, galaxy2 in data.items():
            if galaxy == galaxy2:
                continue
            if (galaxy2, galaxy) in done:
                continue
            dist = manhattan(pos, pos2)
            done.add((galaxy, galaxy2))
            if dist < mins.get((galaxy, galaxy2), float("inf")):
                mins[(galaxy, galaxy2)] = dist

    return sum(mins.values())


def parse2(data):
    lines = {
        (x, y): vy for x, vx in enumerate(data.split("\n")) for y, vy in enumerate(vx)
    }
    col_with_galaxies = set()
    rows_with_galaxies = set()
    galaxies = {}
    n = 1
    for y in range(max(lines, key=lambda x: x[1])[1] + 1):
        for x in range(max(lines, key=lambda x: x[0])[0] + 1):
            if lines[(x, y)] == "#":
                galaxies[(x, y)] = n
                n += 1
                col_with_galaxies.add(y)
                rows_with_galaxies.add(x)

    rows_without_galaxies = (
        set(range(max(lines, key=lambda x: x[0])[0] + 1)) - rows_with_galaxies
    )
    cols_without_galaxies = (
        set(range(max(lines, key=lambda x: x[1])[1] + 1)) - col_with_galaxies
    )

    galaxy_map = {}
    for pos, galaxy in galaxies.items():
        x, y = pos
        x += len([row for row in rows_without_galaxies if row <= x]) * (1e6 - 1)
        y += len([col for col in cols_without_galaxies if col <= y]) * (1e6 - 1)
        galaxy_map[(x, y)] = galaxy

    return galaxy_map


def p2(data=aoc_data):
    data = parse2(data)

    result = 0
    mins = dict()
    done = set()
    for pos, galaxy in data.items():
        for pos2, galaxy2 in data.items():
            if galaxy == galaxy2:
                continue
            if (galaxy2, galaxy) in done:
                continue
            dist = manhattan(pos, pos2)
            done.add((galaxy, galaxy2))
            if dist < mins.get((galaxy, galaxy2), float("inf")):
                mins[(galaxy, galaxy2)] = dist

    return sum(mins.values())


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
