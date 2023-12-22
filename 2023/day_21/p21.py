#! /usr/bin/env python
import functools
import heapq
import operator
import pathlib
from pprint import pprint
import sys
import fire
import collections
import itertools
import more_itertools
import numpy as np

from aocd import data as aoc_data
from aocd import submit


def parse(data):
    return {
        (x, y): vy for x, vx in enumerate(data.split("\n")) for y, vy in enumerate(vx)
    }


def bfs(data, start, steps):
    distances = {}
    distances[start] = 0

    visited = set()
    queue = collections.deque([(0, start)])

    while queue:
        cur_dist, cur = queue.popleft()
        if cur_dist > steps or (cur_dist, cur) in visited:
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
            queue.append((new_path_cost, neighbor))
            distances[neighbor] = new_path_cost

    return distances


def p1(data=aoc_data):
    data = parse(data)

    start = [pos for pos, val in data.items() if val == "S"][0]
    steps = 64
    distances = bfs(data, start, steps)
    return len([pos for pos, distance in distances.items() if distance == steps])


def parse2(data):
    return parse(data)


def bfs_infinite(data, start, steps):
    distances = {}
    distances[start] = 0

    visited = set()
    queue = collections.deque([(0, start)])

    height = max(data, key=operator.itemgetter(0))[0] + 1
    width = max(data, key=operator.itemgetter(1))[1] + 1

    while queue:
        cur_dist, cur = queue.popleft()
        if cur_dist >= steps or (cur_dist, cur) in visited:
            continue

        visited.add((cur_dist, cur))
        r, c = cur

        neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        for neighbor in neighbors:
            if (cur_dist, neighbor) in visited:
                continue
            moduled_neighbor = (
                ((neighbor[0] % height) + width) % width,
                ((neighbor[1] % height) + height) % height,
            )
            if data[moduled_neighbor] == "#":
                continue

            new_path_cost = cur_dist + 1
            queue.append((new_path_cost, neighbor))

            distances[neighbor] = new_path_cost

    return distances


def bfs_infinite_border(data, start, steps):
    distances = {}
    distances[start] = 0

    visited = set()
    queue = collections.deque([(0, start)])

    height = max(data, key=operator.itemgetter(0))[0] + 1
    width = max(data, key=operator.itemgetter(1))[1] + 1

    while queue:
        cur_dist, cur = queue.popleft()
        if cur_dist >= steps or cur in visited:
            continue

        visited.add(cur)
        r, c = cur

        neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        for neighbor in neighbors:
            if neighbor in visited:
                continue
            moduled_neighbor = (
                ((neighbor[0] % height) + width) % width,
                ((neighbor[1] % height) + height) % height,
            )
            if data[moduled_neighbor] == "#":
                continue

            new_path_cost = cur_dist + 1
            queue.append(neighbor)

            distances[neighbor] = new_path_cost

    return distances


def p2(data=aoc_data):
    data = parse2(data)

    start = [pos for pos, val in data.items() if val == "S"][0]
    data[start] == "."

    full_steps = 26501365

    max_x = max(data, key=operator.itemgetter(0))[0] + 1
    max_y = max(data, key=operator.itemgetter(1))[1] + 1

    steps = list(range(max_x // 2, max_x * 3, max_x))
    values = []
    # Noticed that how far bfs_infinite_border got increased linearly with increased steps
    # and reasoned that since the pattern is repeating it should just be a matter of finding how
    # many grids we end up finding. After a long time of trying to find a smart way to find
    # how far we got depending on the number of steps I lucked out in testing if just fitting
    # a second order polynomial to the values of crossing the border twice would work...

    for steps in [6, 10, 50, 100, 500]:
        distances = bfs_infinite(data, start, steps)
        print("steps=", steps)
        print(len([pos for pos, distance in distances.items() if distance == steps]))

        second = collections.Counter()
        layers = set()
        for pos, distance in distances.items():
            x_layer = pos[0] // (max_x + 1)
            y_layer = pos[1] // (max_y + 1)
            second[(x_layer, y_layer)] += 1 if distance == steps else 0

        print(f"{second=}")
        print("=" * 50)
    breakpoint()


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
