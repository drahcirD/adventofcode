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
    lines = {}

    for y, row in enumerate(data.split("\n")):
        for x, v in enumerate(row):
            lines[(x, y)] = v

    return lines


def p1(data=aoc_data):
    data = parse(data)

    result = 0
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    word = "XMAS"

    for pos, val in data.items():
        for d in directions:
            if val != word[0]:
                continue
            x, y = pos
            for i in range(1, 4):
                x += d[0]
                y += d[1]
                pos2 = x, y
                if pos2 not in data or data[x, y] != word[i]:
                    break
            else:
                result += 1

    return result


def parse2(data):
    return parse(data)


def p2(data=aoc_data):
    data = parse2(data)
    result = 0

    for pos, val in data.items():
        if val != "A":
            continue

        x, y = pos

        upleft = x - 1, y - 1
        downleft = x - 1, y + 1
        upright = x + 1, y - 1
        downright = x + 1, y + 1

        if (
            upleft not in data
            or downleft not in data
            or upright not in data
            or downright not in data
        ):
            continue

        if (
            (data[upleft] == "M" and data[downright] == "S")
            or (data[upleft] == "S" and data[downright] == "M")
        ) and (
            (data[downleft] == "M" and data[upright] == "S")
            or (data[downleft] == "S" and data[upright] == "M")
        ):
            result += 1

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
