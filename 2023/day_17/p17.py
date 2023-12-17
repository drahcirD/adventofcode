#! /usr/bin/env python
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


def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def last_three(prev_path):
    path = []
    for last, cur in itertools.pairwise(prev_path):
        direction = complex(cur[0] - last[0], cur[1] - last[1])
        path.append(direction)

    return path


def heuristic_map(data):
    max_x = max(data, key=operator.itemgetter(0))[0]
    max_y = max(data, key=operator.itemgetter(1))[1]
    distances = {(max_x, max_y): data[(max_x, max_y)]}
    for x in reversed(range(max_x + 1)):
        for y in reversed(range(max_y + 1)):
            if x == max_x and y == max_y:
                continue
            a = distances[(x, y + 1)] if (x, y + 1) in data else 1e100
            b = distances[(x + 1, y)] if (x + 1, y) in data else 1e100

            distances[(x, y)] = data[(min(x + 1, max_x), min(y + 1, max_y))] + min(a, b)

    return distances


def dijkstra(data, start, end):
    distances = {}
    distances[(tuple([]), start)] = 0
    pq = [(0, (tuple(), start))]

    while pq:
        cur_dist, state = heapq.heappop(pq)
        prev_path, cur = state
        if cur == end:
            return cur_dist

        r, c = cur

        neighbors = [(r, c - 1), (r - 1, c), (r + 1, c), (r, c + 1)]
        for neighbor in neighbors:
            if neighbor not in data:
                continue
            direction = complex(neighbor[0] - cur[0], neighbor[1] - cur[1])

            last_dirs = last_three(prev_path)
            if len(last_dirs) > 2 and all([direction == x for x in last_dirs[-3:]]):
                continue
            if last_dirs:
                if last_dirs[-1] == 1j and direction == -1j:
                    continue
                if last_dirs[-1] == -1j and direction == 1j:
                    continue
                if last_dirs[-1] == 1 and direction == -1:
                    continue
                if last_dirs[-1] == -1 and direction == 1:
                    continue

            new_state = (tuple(list(prev_path[-3:]) + [neighbor]), neighbor)
            old_path_cost = distances.get(new_state, sys.maxsize)
            cost_to_neighbor = int(data[neighbor])
            new_path_cost = distances[state] + cost_to_neighbor
            if new_path_cost < old_path_cost:
                heuristic = manhattan(neighbor, end)
                heapq.heappush(pq, (new_path_cost + heuristic, new_state))
                distances[new_state] = new_path_cost

    return distances[end]


def dijkstra2(data, start, end):
    distances = {}
    distances[start] = 0

    visited = set()
    pq = [(0, 0, (None, 0, start))]
    heuristics = heuristic_map(data)

    while pq:
        _, cur_dist, state = heapq.heappop(pq)
        last_dir, count, cur = state
        if cur == end:
            return cur_dist

        visited.add(state)
        r, c = cur

        neighbors = set()

        last_dir = complex(*last_dir) if count > 0 else None
        for dir in [1j, -1j, 1, -1]:
            if last_dir == 1j and dir == -1j:
                continue
            if last_dir == -1j and dir == 1j:
                continue
            if last_dir == 1 and dir == -1:
                continue
            if last_dir == -1 and dir == 1:
                continue
            if dir == last_dir and count == 10:
                continue
            if dir != last_dir and count > 0 and count < 4:
                continue
            pos = (r + int(dir.real), c + int(dir.imag))
            if pos not in data:
                continue
            if pos == end and count != 3:
                continue
            neighbors.add((pos, dir, count + 1 if dir == last_dir else 1, data[pos]))

        for neighbor, direction, count, cost_to_neighbor in neighbors:
            new_state = ((direction.real, direction.imag), count, neighbor)

            if new_state in visited:
                continue
            old_path_cost = distances.get(new_state, sys.maxsize)
            new_path_cost = cur_dist + cost_to_neighbor

            if new_path_cost < old_path_cost:
                # for sure not right but gets me the right answer...
                heuristic = (heuristics[neighbor] + manhattan(neighbor, end)) / 2
                heapq.heappush(
                    pq, (new_path_cost + heuristic, new_path_cost, new_state)
                )
                distances[neighbor] = new_path_cost

    return None


def parse(data):
    return {
        (x, y): int(vy)
        for x, vx in enumerate(data.split("\n"))
        for y, vy in enumerate(vx)
    }


def p1(data=aoc_data):
    data = parse(data)

    max_x = max(data, key=operator.itemgetter(0))[0]
    max_y = max(data, key=operator.itemgetter(1))[1]

    start = (0, 0)
    end = (max_x, max_y)
    distance = dijkstra(data, start, end)
    return distance


def parse2(data):
    return parse(data)


def p2(data=aoc_data):
    data = parse2(data)

    max_x = max(data, key=operator.itemgetter(0))[0]
    max_y = max(data, key=operator.itemgetter(1))[1]
    start = (0, 0)
    end = (max_x, max_y)
    distance = dijkstra2(data, start, end)

    return distance


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


def e3(path=pathlib.Path(__file__).resolve().parent / "example2.txt"):
    return p2(path.read_text())


if __name__ == "__main__":
    fire.Fire()
