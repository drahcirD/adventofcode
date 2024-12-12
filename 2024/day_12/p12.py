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
    arr = np.array(
        [
            np.asarray([nbr if nbr != "." else 10 for nbr in row])
            for row in data.split("\n")
        ]
    )
    arr = np.pad(arr, pad_width=1, mode="constant", constant_values=".")
    return arr


def explore(in_region, visited, val, p, array, region):
    if array[p] == "." or p in visited or p in in_region:
        return

    visited.add(p)
    if array[p] == val:
        region.add(p)
        in_region.add(p)
    else:
        return

    r, c = p
    up = r - 1, c
    down = r + 1, c
    left = r, c - 1
    right = r, c + 1
    for new in [up, down, left, right]:
        explore(in_region, visited, val, new, array, region)
    return


def p1(data=aoc_data):
    data = parse(data)

    result = 0
    regions = collections.defaultdict(set)
    in_region = set()
    for c in range(1, data.shape[1] - 1):
        for r in range(1, data.shape[0] - 1):
            pos = r, c
            explore(in_region, set(), data[pos], pos, data, regions[pos])

    for start, region in regions.items():
        if not region:
            continue
        region.add(start)
        perimeter = 0
        area = len(region)
        for pos in region:
            r, c = pos
            up = r - 1, c
            down = r + 1, c
            left = r, c - 1
            right = r, c + 1
            for neighbor in [up, down, left, right]:
                if data[neighbor] != data[pos]:
                    perimeter += 1
        result += perimeter * area
        print(data[pos], area, perimeter)
    return result


def parse2(data):
    return parse(data)

def p2(data=aoc_data):
    data = parse2(data)

    result = 0
    regions = collections.defaultdict(set)
    in_region = set()
    for c in range(1, data.shape[1] - 1):
        for r in range(1, data.shape[0] - 1):
            pos = r, c
            explore(in_region, set(), data[pos], pos, data, regions[pos])

    for start, region in regions.items():
        if not region:
            continue
        region.add(start)
        sides = 0
        area = len(region)

        for pos in region:
            r, c = pos
            up = r - 1, c
            down = r + 1, c
            left = r, c - 1
            right = r, c + 1

            if up not in region and left not in region:
                sides += 1

            if up not in region and right not in region:
                sides += 1

            if down not in region and left not in region:
                sides += 1

            if down not in region and right not in region:
                sides += 1

            if (r + 1, c + 1) not in region and right in region and down in region:
                sides += 1

            if (r + 1, c - 1) not in region and left in region and down in region:
                sides += 1

            if (r - 1, c + 1) not in region and up in region and right in region:
                sides += 1

            if (r - 1, c - 1) not in region and up in region and left in region:
                sides += 1
        result += sides * area

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
