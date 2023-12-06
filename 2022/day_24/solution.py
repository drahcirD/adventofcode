#! /usr/bin/env python
from functools import cache
from heapq import heappop, heappush
import operator
import pathlib
import sys
import fire




def e1(path=pathlib.Path(__file__).resolve().parent / "example.txt"):
    return p1(path)


def e2(path=pathlib.Path(__file__).resolve().parent / "example.txt"):
    return p2(path)


@cache
def get_blizzards(blizzards, max_x, max_y, min_x, min_y):
    new_blizzards = []
    for pos, dir, id_ in blizzards:
        match dir:
            case "^":
                new = (pos[0], pos[1] - 1)
                if new[1] == min_y:
                    new = (pos[0], max_y - 1)
            case "v":
                new = (pos[0], pos[1] + 1)
                if new[1] == max_y:
                    new = (pos[0], min_y + 1)
            case ">":
                new = (pos[0] + 1, pos[1])
                if new[0] == max_x:
                    new = (min_x + 1, pos[1])
            case "<":
                new = (pos[0] - 1, pos[1])
                if new[0] == min_x:
                    new = (max_x - 1, pos[1])
        new_blizzards.append((new, dir, id_))
    return frozenset(new_blizzards)

@cache
def get_pos(pos):
    new_pos = []
    directions = [(1, 0), (-1, 0), (0, 0), (0, 1), (0, -1)] 
    for dir in directions:
        new = (pos[0] + dir[0], pos[1] + dir[1])
        new_pos.append(new)
    return new_pos

def dijkstra(graph, start, end, blizzards):
    distances = {}
    distances[(start, blizzards)] = 0
    max_x = max(graph, key=operator.itemgetter(0))[0]
    max_y = max(graph, key=operator.itemgetter(1))[1]
    min_x = min(graph, key=operator.itemgetter(0))[0]
    min_y = min(graph, key=operator.itemgetter(1))[1]
    boundaries = {k for k,v in graph.items() if v == '#'}
    boundaries.add((1,-1))
    boundaries.add((max_x - 1, max_y+1))

    pq = []
    pq.append((abs(start[0] - end[0]) + abs(start[1] - end[1]), 0, (start, blizzards)))

    while pq:
        (_, cur_dist, cur) = heappop(pq)
        if cur[0] == end:
            return (cur,cur_dist)
        if cur_dist > distances.get(cur, sys.maxsize):
            continue

        new_blizzards = get_blizzards(cur[1], max_x, max_y, min_x, min_y)
        new_pos = get_pos(cur[0], start, end, max_x, max_y, min_x, min_y)
        
        blizzards_pos = set([b[0] for b in new_blizzards])
        for pos in new_pos:
            if pos in blizzards_pos or pos in boundaries:
                continue

            neighbor = (pos, new_blizzards)
            old_path_cost = distances.get(neighbor, sys.maxsize)
            new_path_cost = cur_dist + 1
            if new_path_cost < old_path_cost:
                heappush(pq, (new_path_cost+(abs(pos[0] - end[0]) + abs(pos[1] - end[1])), new_path_cost, neighbor))
                distances[neighbor] = new_path_cost


def p1(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [x for x in path.read_text().split("\n")]
        elves = {}
        for i, row in enumerate(lines):
            for j, col in enumerate(row):
                elves[(j, i)] = col

        return elves

    def solve(graph):
        max_x = max(graph, key=operator.itemgetter(0))[0]
        max_y = max(graph, key=operator.itemgetter(1))[1]
        min_x = min(graph, key=operator.itemgetter(0))[0]
        min_y = min(graph, key=operator.itemgetter(1))[1]
        start = (1, 0)
        end = (max_x - 1, max_y)

        blizzards = frozenset(
            [
                (k, v, i)
                for i, (k, v) in enumerate(graph.items())
                if v in {">", "<", "v", "^"}
            ]
        )
        res = dijkstra(graph, start, end, blizzards)

        return res[1]

    return solve(parse())


def p2(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [x for x in path.read_text().split("\n")]
        elves = {}
        for i, row in enumerate(lines):
            for j, col in enumerate(row):
                elves[(j, i)] = col

        return elves

    def solve(graph):
        max_x = max(graph, key=operator.itemgetter(0))[0]
        max_y = max(graph, key=operator.itemgetter(1))[1]
        min_x = min(graph, key=operator.itemgetter(0))[0]
        min_y = min(graph, key=operator.itemgetter(1))[1]
        start = (1, 0)
        end = (max_x - 1, max_y)

        blizzards = frozenset(
            [
                (k, v, i)
                for i, (k, v) in enumerate(graph.items())
                if v in {">", "<", "v", "^"}
            ]
        )
        res = dijkstra(graph, start, end, blizzards)
        print(res[1])
        res2 = dijkstra(graph, end, start, res[0][1])
        print(res2[1])
        res3 = dijkstra(graph, start, end, res2[0][1])
        return res[1]+ res2[1] + res3[1]

    return solve(parse())


def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": p1(example), "input": p1()},
        "part2": {"example": p2(example), "input": p2()},
    }


if __name__ == "__main__":
    fire.Fire()
