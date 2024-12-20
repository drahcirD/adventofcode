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
    return np.array([np.asarray([x for x in row]) for row in data.split("\n")])


def bfs(data, start, end):
    distances = {}
    distances[start[0], start[1]] = 0
    height, width = data.shape

    visited = set()
    queue = collections.deque([(0, start[0], start[1])])

    while queue:
        cur_dist, r, c = queue.popleft()
        if (cur_dist, r, c) in visited:
            continue

        if (r, c) == end:
            continue

        visited.add((cur_dist, r, c))

        neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]

        for neighbor in neighbors:
            rn, cn = neighbor

            if rn <= 0 or rn >= height or cn <= 0 or cn >= width:
                continue
            if (cur_dist, rn, cn) in visited:
                continue

            if data[rn, cn] == "#":
                continue

            new_path_cost = cur_dist + 1
            if new_path_cost < distances.get((rn, cn), float("inf")):
                queue.append((new_path_cost, rn, cn))
                distances[(rn, cn)] = new_path_cost

    return distances


def p1(data=aoc_data):
    data = parse(data)

    height, width = data.shape

    start = None
    end = None
    for r in range(height):
        for c in range(width):
            if data[r, c] == "S":
                start = (r, c)
                break
            if data[r, c] == "E":
                end = (r, c)
                break
        if start and end:
            break

    dists = bfs(data, start, end)

    cheats = []
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            if data[r, c] == "#":
                neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
                points = [neighbor for neighbor in neighbors if data[neighbor] in {".", "S", "E"}]

                for a, b in itertools.combinations(points, 2):
                    rd, cd = a[0] - b[0], a[1] - b[1]
                    if rd == 0 or cd == 0:
                        cheats.append(abs(dists[a] - dists[b]) - 2)

    return len([cheat for cheat in cheats if cheat >= 100])


def parse2(data):
    return parse(data)


def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def p2(data=aoc_data):
    data = parse2(data)

    height, width = data.shape

    start = None
    end = None
    for r in range(height):
        for c in range(width):
            if data[r, c] == "S":
                start = (r, c)
                break
            if data[r, c] == "E":
                end = (r, c)
                break
        if start and end:
            break

    dists = bfs(data, start, end)

    result = 0

    for a, b in itertools.combinations(dists.items(), 2):
        pa, da = a
        pb, db = b
        if manhattan(pa, pb) > 20:
            continue
        cheat = abs(da - db) - manhattan(pa, pb)
        if cheat >= 100:
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
