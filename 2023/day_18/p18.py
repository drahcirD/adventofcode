#! /usr/bin/env python
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
import matplotlib


def parse(data):
    lines = [x for x in data.split("\n")]
    return lines


def print_room(room):
    for x in range(max(room, key=lambda x: x[0])[0] + 1):
        for y in range(max(room, key=lambda x: x[1])[1] + 1):
            try:
                print(room[(x, y)], end="")
            except:
                print(".", end="")
        print()


def p1(data=aoc_data):
    data = parse(data)

    map = {}
    pos = (0, 0)
    path = [pos]
    for d in data:
        direction, length, _ = d.split(" ")
        map[pos] = "#"

        if direction == "R":
            direction = (0, 1)
        elif direction == "L":
            direction = (0, -1)
        elif direction == "U":
            direction = (-1, 0)
        elif direction == "D":
            direction = (1, 0)
        for i in range(int(length)):
            pos = (pos[0] + direction[0], pos[1] + direction[1])
            map[pos] = "#"
            path.append(pos)

    max_x = max(map, key=operator.itemgetter(0))[0]
    max_y = max(map, key=operator.itemgetter(1))[1]
    min_x = min(map, key=operator.itemgetter(0))[0]
    min_y = min(map, key=operator.itemgetter(1))[1]

    lib_path = matplotlib.path.Path(path)
    inside = set()
    for i in range(min_x, max_x + 3):
        for j in range(min_y, max_y + 3):
            if lib_path.contains_point((i, j)):
                inside.add((i, j))
                map[(i, j)] = "#"

    return len(map)


def parse2(data):
    return parse(data)


def p2(data=aoc_data):
    data = parse2(data)
    pos = (0, 0)
    area = 0
    prev_pos = pos
    n = 0
    for d in tqdm.tqdm(data):
        _, _, color = d.split(" ")

        length = int(color[2:7], 16)
        direction = color[7:-1]

        if direction == "0":
            direction = (0, 1)
        elif direction == "2":
            direction = (0, -1)
        elif direction == "3":
            direction = (-1, 0)
        elif direction == "1":
            direction = (1, 0)
        for i in range(int(length)):
            pos = (pos[0] + direction[0], pos[1] + direction[1])
            # shoelace formula
            area += prev_pos[0] * pos[1]
            area -= pos[0] * prev_pos[1]
            prev_pos = pos
            n += 1
    return abs(area) / 2 + n // 2 + 1


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
