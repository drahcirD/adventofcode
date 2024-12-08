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
    lines = {}

    for y, row in enumerate(data.split("\n")):
        for x, v in enumerate(row):
            lines[(x, y)] = v

    return lines


def p1(data=aoc_data):
    data = parse(data)

    result = 0
    antenna_types = set(data.values()) - {"."}
    locations = collections.defaultdict(list)
    for pos, a in data.items():
        if a == ".":
            continue
        locations[a].append(pos)

    max_x = max(data, key=operator.itemgetter(0))[0]
    max_y = max(data, key=operator.itemgetter(1))[1]
    antinodes = set()
    for a in antenna_types:
        for p1, p2 in itertools.combinations(locations[a], r=2):
            xdist = p1[0] - p2[0]
            ydist = p1[1] - p2[1]

            antip1 = p1[0] + xdist, p1[1] + ydist
            antip2 = p2[0] - xdist, p2[1] - ydist

            if max_x >= antip1[0] >= 0 and max_y >= antip1[1] >= 0:
                antinodes.add(antip1)
            if max_x >= antip2[0] >= 0 and max_y >= antip2[1] >= 0:
                antinodes.add(antip2)

    result += len(antinodes)
    return result


def parse2(data):
    return parse(data)


def p2(data=aoc_data):
    data = parse2(data)

    result = 0
    antenna_types = set()
    locations = collections.defaultdict(list)
    for pos, a in data.items():
        if a == ".":
            continue
        locations[a].append(pos)
        antenna_types.add(a)

    max_x = max(data, key=operator.itemgetter(0))[0]
    max_y = max(data, key=operator.itemgetter(1))[1]
    antinodes = set()
    for a in antenna_types:
        for p1, p2 in itertools.combinations(locations[a], r=2):
            xdist = p1[0] - p2[0]
            ydist = p1[1] - p2[1]
            new = True
            i = 0
            while new:
                new = False
                antip1 = p1[0] + i * xdist, p1[1] + i * ydist
                antip2 = p2[0] - i * xdist, p2[1] - i * ydist

                if max_x >= antip1[0] >= 0 and max_y >= antip1[1] >= 0:
                    new = True
                    antinodes.add(antip1)
                if max_x >= antip2[0] >= 0 and max_y >= antip2[1] >= 0:
                    new = True
                    antinodes.add(antip2)
                i += 1

    result += len(antinodes)
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
