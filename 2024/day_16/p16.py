#! /usr/bin/env python
import operator
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


def bfs(data, start, dir, end):
    distances = {}
    distances[start[0], start[1], dir[0], dir[1]] = 0
    height, width = data.shape

    visited = set()
    queue = collections.deque([(0, start[0], start[1], dir[0], dir[1])])

    while queue:
        cur_dist, r, c, rd, cd = queue.popleft()
        if (cur_dist, r, c, rd, cd) in visited:
            continue

        if (r, c) == end:
            continue

        visited.add((cur_dist, r, c, rd, cd))

        complex_dir = complex(rd, cd)

        neighbors = [
            (1, r + rd, c + cd, rd, cd),
        ]
        for rot in [complex(0, 1), complex(0, -1)]:
            new_dir = complex_dir * rot
            neighbors.append((1000, r, c, int(new_dir.real), int(new_dir.imag)))

        for neighbor in neighbors:
            score, rn, cn, rdn, rcn = neighbor

            if rn < 0 or rn > height or cn < 0 or cn > width:
                continue
            if (cur_dist, rn, cn, rdn, rcn) in visited:
                continue

            if data[rn, cn] == "#":
                continue

            new_path_cost = cur_dist + score
            if new_path_cost < distances.get((rn, cn, rdn, rcn), float("inf")):
                queue.append((new_path_cost, rn, cn, rdn, rcn))
                distances[(rn, cn, rdn, rcn)] = new_path_cost

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

    dists = bfs(data, start, (0, 1), end)
    end_dists = []
    for s, d in dists.items():
        if (s[0], s[1]) == end:
            end_dists.append(d)

    return min(end_dists)


def parse2(data):
    return parse(data)


def search_backwards(data, start, dir, end, min_dists):
    height, width = data.shape

    queue = collections.deque([(0, start[0], start[1], dir[0], dir[1])])
    seats = set()
    reversed_dir = complex(dir[0], dir[1]) * 1j * 1j
    start_cost = min_dists[*start, int(reversed_dir.real), int(reversed_dir.imag)]
    while queue:
        cur_dist, r, c, rd, cd = queue.popleft()

        seats.add((r, c))
        if (r, c) == end:
            continue

        complex_dir = complex(rd, cd)

        neighbors = [
            (1, r + rd, c + cd, rd, cd),
        ]
        for rot in [complex(0, 1), complex(0, -1)]:
            new_dir = complex_dir * rot
            neighbors.append((1000, r, c, int(new_dir.real), int(new_dir.imag)))

        for neighbor in neighbors:
            score, rn, cn, rdn, cdn = neighbor

            if rn < 0 or rn > height or cn < 0 or cn > width:
                continue

            if data[rn, cn] == "#":
                continue

            new_path_cost = cur_dist + score
            reversed_dir = complex(rdn, cdn) * 1j * 1j
            new_state = rn, cn, int(reversed_dir.real), int(reversed_dir.imag)
            if (
                new_state not in min_dists
                or min_dists[rn, cn, int(reversed_dir.real), int(reversed_dir.imag)]
                != start_cost - new_path_cost
            ):
                continue
            queue.append((new_path_cost, rn, cn, rdn, cdn))
    return len(seats)


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
    dists = bfs(data, start, (0, 1), end)

    paths = []
    min_dists = {}
    for s, d in dists.items():
        if s in min_dists:
            min_dists[s] = min(min_dists[s], d)
        else:
            min_dists[s] = d

        if (s[0], s[1]) == end:
            paths.append((s, d, None))
    state, _, _ = min(paths, key=operator.itemgetter(1))
    _, _, rd, cd = state
    reversed_dir = complex(rd, cd) * 1j * 1j

    dists = search_backwards(
        data, end, (int(reversed_dir.real), int(reversed_dir.imag)), start, min_dists
    )
    return dists


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
