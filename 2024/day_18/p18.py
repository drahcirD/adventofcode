#! /usr/bin/env python
import copy
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
    lines = [x for x in data.split("\n")]
    return lines


def bfs(data, start, end):
    distances = {}
    distances[start] = 0

    visited = set()
    queue = collections.deque([(0, start)])

    while queue:
        cur_dist, cur = queue.popleft()
        if (cur_dist, cur) in visited:
            continue

        visited.add((cur_dist, cur))
        r, c = cur

        neighbors = set()

        neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        for neighbor in neighbors:
            if neighbor not in data:
                continue
            if (cur_dist, neighbor) in visited:
                continue
            if data[neighbor] == "#":
                continue

            new_path_cost = cur_dist + 1
            if new_path_cost < distances.get(neighbor, float("inf")):
                queue.append((new_path_cost, neighbor))
                distances[neighbor] = new_path_cost
    return distances


def p1(data=aoc_data):
    data = parse(data)

    if len(data) < 50:
        gridy = 6
        gridx = 6
        bytes = 12
    else:
        gridy = 70
        gridx = 70
        bytes = 1024

    map = {}
    for r in range(gridy + 1):
        for c in range(gridx + 1):
            map[(r, c)] = "."

    for i in range(bytes):
        x, y = data[i].split(",")
        map[(int(x), int(y))] = "#"

    start = (0, 0)
    end = (gridx, gridy)

    dists = bfs(map, start, end)

    return dists[end]


def parse2(data):
    return parse(data)


def p2(data=aoc_data):
    data = parse2(data)

    if len(data) < 50:
        gridy = 6
        gridx = 6
        orig_bytes = 12
    else:
        gridy = 70
        gridx = 70
        orig_bytes = 1024

    map = {}
    for r in range(gridy + 1):
        for c in range(gridx + 1):
            map[(r, c)] = "."

    orig_map = copy.deepcopy(map)

    start = (0, 0)
    end = (gridy, gridx)

    all_bytes = len(data)

    left, right = orig_bytes, all_bytes
    while right > left:
        bytes = (left + right) // 2
        map = copy.deepcopy(orig_map)

        for i in range(bytes + 1):
            x, y = data[i].split(",")
            map[(int(x), int(y))] = "#"

        dists = bfs(map, start, end)
        if end in dists:
            left = bytes + 1
        else:
            right = bytes
    assert left == right
    return data[left]


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
