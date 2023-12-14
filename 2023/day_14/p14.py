#! /usr/bin/env python
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
    def translate(c):
        if c == "#":
            return 1
        if c == "O":
            return 2

        return 0

    pattern = [[translate(v) for v in row] for row in data.split("\n")]
    pattern = np.array([np.array(line) for line in pattern])
    return pattern


def p1(data=aoc_data):
    data = parse(data)

    result = 0

    indices = zip(*np.where(data == 2))
    for i, j in indices:
        while True:
            if i - 1 < 0 or data[i - 1, j] == 1 or data[i - 1, j] == 2:
                break

            data[i - 1, j], data[i, j] = data[i, j], data[i - 1, j]
            i -= 1
    indices = zip(*np.where(data == 2))

    return sum([data.shape[0] - x for x, _ in indices])


def parse2(data):
    return parse(data)


def p2(data=aoc_data):
    data = parse2(data)

    indices = frozenset(zip(*np.where(data == 2)))
    datas = set()
    first = None
    cycle = None
    done = False
    for rounds in range(1000000000):
        if done:
            break
        datas.add(frozenset(indices))
        for direction in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            for i, j in sorted(
                indices,
                key=lambda x: -x[0] * direction[0]
                if direction[0]
                else -x[1] * direction[1],
            ):
                while True:
                    new_i = i + direction[0]
                    new_j = j + direction[1]

                    if not (data.shape[0] > new_i >= 0):
                        break
                    if not (data.shape[1] > new_j >= 0):
                        break
                    if data[new_i, new_j] == 1 or data[new_i, new_j] == 2:
                        break
                    data[new_i, new_j], data[i, j] = data[i, j], data[new_i, new_j]
                    i = new_i
                    j = new_j
            indices = frozenset(zip(*np.where(data == 2)))
        if indices in datas:
            if not first:
                first = rounds
            if not cycle:
                cycle = rounds - first
            if first and cycle:
                done = True
            datas = set()

    for round in range((1000000000 - first) % cycle - 1):
        for direction in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            for i, j in sorted(
                indices,
                key=lambda x: -x[0] * direction[0]
                if direction[0]
                else -x[1] * direction[1],
            ):
                while True:
                    new_i = i + direction[0]
                    new_j = j + direction[1]
                    # breakpoint()

                    if not (data.shape[0] > new_i >= 0):
                        break
                    if not (data.shape[1] > new_j >= 0):
                        break
                    if data[new_i, new_j] == 1 or data[new_i, new_j] == 2:
                        break
                    data[new_i, new_j], data[i, j] = data[i, j], data[new_i, new_j]
                    i = new_i
                    j = new_j
            indices = frozenset(zip(*np.where(data == 2)))

    indices = zip(*np.where(data == 2))
    return sum([data.shape[0] - x for x, _ in indices])


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
