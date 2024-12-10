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
    return np.array(
        [
            np.asarray([int(nbr) if nbr != "." else 10 for nbr in row])
            for row in data.split("\n")
        ]
    )


def dfs(cur, p, array, nines):
    if array[p] - cur != 1 or array[p] == 10:
        return

    if array[p] == 9:
        nines.add(p)

    r, c = p
    up = r - 1, c
    down = r + 1, c
    left = r, c - 1
    right = r, c + 1
    for new in [up, down, left, right]:
        dfs(array[p], new, array, nines)
    return


def p1(data=aoc_data):
    data = parse(data)

    result = 0

    array = np.pad(data, pad_width=1, mode="constant", constant_values=10)
    heads = []
    for c in range(1, array.shape[1] - 1):
        for r in range(1, array.shape[0] - 1):
            if array[r, c] == 0:
                heads.append((r, c))

    for r, c in heads:
        up = r - 1, c
        down = r + 1, c
        left = r, c - 1
        right = r, c + 1
        nines = set()
        for new in [up, down, left, right]:
            dfs(array[r, c], new, array, nines)
        result += len(nines)

    return result


def dfs_all(cur, p, array, paths):
    if array[p] - cur != 1:
        return 0

    if array[p] == 9:
        return 1

    r, c = p
    up = r - 1, c
    down = r + 1, c
    left = r, c - 1
    right = r, c + 1
    n_paths = paths
    for new in [up, down, left, right]:
        n_paths += dfs_all(array[p], new, array, paths)
    return n_paths


def parse2(data):
    return parse(data)


def p2(data=aoc_data):
    data = parse2(data)

    result = 0

    array = np.pad(data, pad_width=1, mode="constant", constant_values=10)
    heads = []
    for c in range(1, array.shape[1] - 1):
        for r in range(1, array.shape[0] - 1):
            if array[r, c] == 0:
                heads.append((r, c))

    for r, c in heads:
        up = r - 1, c
        down = r + 1, c
        left = r, c - 1
        right = r, c + 1
        for new in [up, down, left, right]:
            result += dfs_all(array[r, c], new, array, 0)

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
