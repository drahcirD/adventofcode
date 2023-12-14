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
    return data.split("\n\n")


def p1(data=aoc_data):
    data = parse(data)

    result = 0

    for pattern in data:
        pattern = [[1 if v == "#" else 0 for v in row] for row in pattern.split("\n")]
        pattern = np.array([np.array(line) for line in pattern])
        rows, cols = pattern.shape
        for row in range(rows):
            mid = rows // 2
            if row > mid:
                down = pattern[row:, :]
                size = down.shape
                up = pattern[row - size[0] : row, :]
            else:
                up = pattern[:row, :]
                size = up.shape
                down = pattern[row : row + size[0], :]

            if (np.flipud(up) == down).all():
                result += 100 * (row)

        for col in range(cols):
            mid = cols // 2
            if col > mid:
                right = pattern[:, col:]
                size = right.shape
                left = pattern[:, col - size[1] : col]
            else:
                left = pattern[:, :col]
                size = left.shape
                right = pattern[:, col : col + size[1]]

            if (np.fliplr(left) == right).all():
                result += col

    return result


def parse2(data):
    return parse(data)


def p2(data=aoc_data):
    data = parse2(data)

    result = 0

    for pattern in data:
        pattern = [[1 if v == "#" else 0 for v in row] for row in pattern.split("\n")]
        pattern = np.array([np.array(line) for line in pattern])
        rows, cols = pattern.shape
        for row in range(rows):
            mid = rows // 2
            if row > mid:
                down = pattern[row:, :]
                size = down.shape
                up = pattern[row - size[0] : row, :]
            else:
                up = pattern[:row, :]
                size = up.shape
                down = pattern[row : row + size[0], :]

            if np.count_nonzero(np.flipud(up) == down) == up.size - 1:
                result += 100 * (row)

        for col in range(cols):
            mid = cols // 2
            if col > mid:
                right = pattern[:, col:]
                size = right.shape
                left = pattern[:, col - size[1] : col]
            else:
                left = pattern[:, :col]
                size = left.shape
                right = pattern[:, col : col + size[1]]

            if np.count_nonzero(np.fliplr(left) == right) == left.size - 1:
                result += col

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
