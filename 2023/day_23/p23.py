#! /usr/bin/env python
import heapq
import operator
import pathlib
from pprint import pprint
import sys

import tqdm
import fire
import collections
import itertools
import more_itertools
import numpy as np

from aocd import data as aoc_data
from aocd import submit


def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def parse(data):
    return {
        (x, y): vy for x, vx in enumerate(data.split("\n")) for y, vy in enumerate(vx)
    }

def dijkstra(data, start, end):
    distances = {}
    distances[start] = 0
    pq = [(0, (frozenset([start]), start))]
    seen = set()
    cur_max = 0
    i = 0
    while pq:
        i+=1
        cur_dist, state = heapq.heappop(pq)
        path, cur = state
        if cur == end:
            # return cur_dist
            cur_max = max(abs(cur_dist)-1, cur_max)
            print(cur_max)
            # print_room(data, path)
            # breakpoint()

        if i % 10000 == 0:
            print("len=", len(pq))
        r, c = cur

        neighbors = [(r, c - 1), (r - 1, c), (r + 1, c), (r, c + 1)]
        for neighbor in neighbors:
            if neighbor not in data:
                continue
            if neighbor in path:
                continue
            new_path = frozenset(path).union(frozenset([neighbor]))
            new_state = (new_path, neighbor)

            # direction = complex(neighbor[0] - cur[0], neighbor[1] - cur[1])

            # if data[neighbor] == '<' and direction != -1j:
            #     continue
            # if data[neighbor] == '>' and direction != 1j:
            #     continue
            # if data[neighbor] == '^' and direction != -1:
            #     continue
            # if data[neighbor] == 'v' and direction != 1:
            #     continue

            old_path_cost = distances.get(neighbor, sys.maxsize)
            new_path_cost = -len(new_path)
            # if new_path_cost < old_path_cost:
            #     heuristic = -0
            heapq.heappush(pq, (new_path_cost, new_state))
                # distances[neighbor] = new_path_cost

    return cur_max

def dijkstra_junction(data, junctions, start, end):
    distances = {}
    distances[start] = 0
    pq = [(0, (frozenset([start]), start))]
    seen = set()
    max_path = None
    cur_max = 0

    while pq:
        cur_dist, state = heapq.heappop(pq)
        path, cur = state
        if cur == end:
            if abs(cur_dist) > cur_max:
                max_path = path
            cur_max = max(abs(cur_dist)-1, cur_max)
            continue
        r, c = cur

        neighbors = [(r, c - 1), (r - 1, c), (r + 1, c), (r, c + 1)]
        for neighbor in neighbors:
            if neighbor not in data:
                continue
            if neighbor in path:
                continue
            

            if neighbor in junctions:
                if neighbor != end:
                    continue
            new_path = frozenset(path).union(frozenset([neighbor]))
            new_state = (new_path, neighbor)

            new_path_cost = len(new_path)
            heapq.heappush(pq, (new_path_cost, new_state))


    return cur_max, max_path

def dijkstra_junction2(data, start, end):
    distances = {}
    distances[start] = 0
    pq = [(0, 0, (frozenset(), tuple([start]), start))]

    cur_max = 0
    seen = set()
    while pq:
        prio, cur_dist, state = heapq.heappop(pq)
        visited, path, cur = state
        if cur == end:
            cur_max = max(abs(cur_dist), cur_max)
            print(cur_max)
            continue
        r, c = cur

        if path in seen:
            continue

        seen.add(path)

        neighbors = data[cur]
        for neighbor, neighbor_path in neighbors.items():
            if neighbor not in data or neighbor in visited:
                continue
            length, neighbor_path = neighbor_path
            if len(neighbor_path & visited) > 1:
                continue
            new_path = tuple(list(path) + [neighbor])
            if new_path in seen:
                continue
            new_visited = frozenset(visited).union(neighbor_path)

            new_state = (new_visited, new_path, neighbor)

            new_path_cost = cur_dist - length

            heapq.heappush(pq, (new_path_cost - max([x[0] for x in data[cur].values()]),  new_path_cost, new_state))


    return cur_max

def p1(data=aoc_data):
    data = parse(data)

    result = 0
    max_x = max(data, key=operator.itemgetter(0))[0]
    max_y = max(data, key=operator.itemgetter(1))[1]
    min_x = min(data, key=operator.itemgetter(0))[0]
    min_y = min(data, key=operator.itemgetter(1))[1]
    data = {pos: val for pos,val in data.items() if val != '#'}
    start = [pos for pos, val in data.items() if val == "." and pos[0]==0][0]
    end = [pos for pos, val in data.items() if val == "." and pos[0]==max_x][0]

    return abs(dijkstra(data, start, end))


def parse2(data):
    return parse(data)

def print_room(room, path):
    for x in range(max(room, key=lambda x: x[0])[0] + 1):
        for y in range(max(room, key=lambda x: x[1])[1] + 1):
            if (x,y) in path:
                print('O', end="")
                continue
            try:
                print(room[(x, y)], end="")
            except:
                print("#", end="")
        print()

def p2(data=aoc_data):
    data = parse2(data)

    result = 0
    max_x = max(data, key=operator.itemgetter(0))[0]
    max_y = max(data, key=operator.itemgetter(1))[1]
    min_x = min(data, key=operator.itemgetter(0))[0]
    min_y = min(data, key=operator.itemgetter(1))[1]
    data = {pos: val for pos,val in data.items() if val != '#'}
    start = [pos for pos, val in data.items() if val == "." and pos[0]==0][0]
    end = [pos for pos, val in data.items() if val == "." and pos[0]==max_x][0]

    junctions = {}
    for pos, val in data.items():
        r,c = pos
        neighbors = [(r, c - 1), (r - 1, c), (r + 1, c), (r, c + 1)]
        count = 0
        for neighbor in neighbors:
            if neighbor in data:
                count += 1
        if count > 2:
            print(pos, val)
            junctions[pos] = {}
    
    for junction in tqdm.tqdm(junctions):
        for next_junction in junctions:
            if junction == next_junction:
                continue
            length, path = dijkstra_junction(data, junctions, junction, next_junction)
            if sys.maxsize > length > 0:
                junctions[junction][next_junction] = (length, path)

    junctions[start] = {}
    junctions[end] = {}
    for junction in tqdm.tqdm(junctions):
        length, path = dijkstra_junction(data, junctions, start, junction)
        length2, path2 = dijkstra_junction(data, junctions, junction, end)

        if sys.maxsize > length > 0:
            junctions[start][junction] = (length, path)
        if sys.maxsize > length2 > 0:

            junctions[junction][end] = (length2, path2)

    return dijkstra_junction2(junctions, start, end)


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
