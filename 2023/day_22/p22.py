#! /usr/bin/env python
import copy
from dataclasses import dataclass
import operator
import pathlib
from pprint import pprint

import tqdm
import fire
import collections
import itertools
import more_itertools
import numpy as np

from aocd import data as aoc_data
from aocd import submit


def parse(data):
    lines = [x for x in data.split("\n")]
    return lines


@dataclass
class Cube:
    x1: int
    y1: int
    z1: int
    x2: int
    y2: int
    z2: int

    @property
    def positions(self):
        for x in range(self.x1, self.x2 + 1):
            for y in range(self.y1, self.y2 + 1):
                for z in range(self.z1, self.z2 + 1):
                    yield (x, y, z)

    @property
    def bottom(self):
        for x in range(self.x1, self.x2 + 1):
            for y in range(self.y1, self.y2 + 1):
                yield (x, y, self.z1)

    @property
    def top(self):
        for x in range(self.x1, self.x2 + 1):
            for y in range(self.y1, self.y2 + 1):
                yield (x, y, self.z2)

    def fall(self):
        self.z1 -= 1
        self.z2 -= 1


def p1(data=aoc_data):
    data = parse(data)

    result = 0
    cubes = []
    positions = {}

    for d in data:
        a, b = d.split("~")

        x1, y1, z1 = [int(x) for x in a.split(",")]
        x2, y2, z2 = [int(x) for x in b.split(",")]
        cubes.append(Cube(x1, y1, z1, x2, y2, z2))

    for i, cube in enumerate(cubes):
        for pos in cube.positions:
            positions[pos] = i

    last_positions = None
    while last_positions != positions:
        last_positions = positions.copy()
        for i, cube in enumerate(cubes):
            if cube.z1 == 1:
                continue
            for pos in cube.positions:
                del positions[pos]

            while cube.z1 > 1 and not any(
                (x, y, z - 1) in positions for x, y, z in cube.bottom
            ):
                cube.fall()

            for pos in cube.positions:
                positions[pos] = i

    supported_by = collections.defaultdict(set)
    supports = collections.defaultdict(set)
    for i, cube in enumerate(cubes):
        for pos in cube.top:
            x, y, z = pos
            if (x, y, z + 1) in positions:
                supp = positions[(x, y, z + 1)]
                supports[i].add(supp)
                supported_by[supp].add(i)

    for i, cube in enumerate(cubes):
        only_support = 0
        for supported in supports[i]:
            if not (supported_by[supported] - {i}):
                only_support += 1
        if only_support == 0:
            result += 1

    return result


def parse2(data):
    return parse(data)


def p2(data=aoc_data):
    data = parse2(data)

    result = 0
    cubes = []
    positions = {}

    for d in data:
        a, b = d.split("~")

        x1, y1, z1 = [int(x) for x in a.split(",")]
        x2, y2, z2 = [int(x) for x in b.split(",")]
        cubes.append(Cube(x1, y1, z1, x2, y2, z2))

    for i, cube in enumerate(cubes):
        for pos in cube.positions:
            positions[pos] = i

    def run_fall(cubes, positions):
        last_positions = None
        fell = set()
        while last_positions != positions:
            last_positions = positions.copy()
            for i, cube in enumerate(cubes):
                if cube.z1 == 1:
                    continue
                for pos in cube.positions:
                    del positions[pos]

                while cube.z1 > 1 and not any(
                    (x, y, z - 1) in positions for x, y, z in cube.bottom
                ):
                    cube.fall()
                    fell.add(i)

                for pos in cube.positions:
                    positions[pos] = i
        return len(fell), positions

    _, positions = run_fall(cubes, positions)

    for cube in tqdm.tqdm(cubes):
        new_cubes = [copy.deepcopy(c) for c in cubes if c != cube]
        new_pos = positions.copy()
        for pos in cube.positions:
            del new_pos[pos]
        result += run_fall(new_cubes, new_pos)[0]
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
