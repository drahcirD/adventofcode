#! /usr/bin/env python
import operator
import pathlib
from queue import PriorityQueue
import sys
import fire


def dijkstra(data, start, flows, n, time=30):
    distances = {}
    distances[start] = 0

    visited = set()
    pq = PriorityQueue()
    pq.put((0, start))

    while not pq.empty():
        (cur_dist, cur) = pq.get()
        print(cur)
        if cur in visited or cur[2] >= time or len(cur[1]) >= n:
            continue
        visited.add(cur)
        for neighbor in data[cur[0]]:

            old_path_cost = distances.get((neighbor, cur[1], cur[2]), sys.maxsize)
            if neighbor not in cur[1] and flows[neighbor] > 0:
                t = cur[2] + 2
                cost = -(time - t) * flows[neighbor] if t <= time else 0
                opened = cur[1].union(set([neighbor]))
            else:
                opened = frozenset(cur[1])
                cost = 0
                t = cur[2] + 1

            neighbor_state = (neighbor, opened, t)
            new_path_cost = cur_dist + cost
            if new_path_cost < old_path_cost:
                pq.put((new_path_cost, neighbor_state))
                distances[neighbor_state] = new_path_cost
    return distances


def p1(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [
            x.replace("=", " ").replace(";", " ").replace(",", " ").split()
            for x in path.read_text().split("\n")
        ]
        flows = {}
        graph = {}
        for line in lines:
            flows[line[1]] = int(line[5])
            graph[line[1]] = line[10:]
        return graph, flows

    def solve(graph, flows):
        dist = dijkstra(
            graph,
            ("AA", frozenset(), 0),
            flows,
            len([flow for flow in flows.values() if flow > 0]),
            time=30,
        )
        return abs(min(dist.values()))

    return solve(*parse())


def p2(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [
            x.replace("=", " ").replace(";", " ").replace(",", " ").split()
            for x in path.read_text().split("\n")
        ]
        flows = {}
        graph = {}
        for line in lines:
            flows[line[1]] = int(line[5])
            graph[line[1]] = line[10:]
        return graph, flows

    def solve(graph, flows):
        dist = dijkstra(
            graph,
            ("AA", frozenset(), 0),
            flows,
            len([flow for flow in flows.values() if flow > 0]),
            time=26,
        )
        min_state = min(dist, key=dist.get)
        dist2 = min(
            [
                (state, value)
                for state, value in dist.items()
                if not state[1].intersection(min_state[1])
            ],
            key=operator.itemgetter(1),
        )
        return abs(dist[min_state] + dist2[1])

    return solve(*parse())


def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": p1(example), "input": p1()},
        "part2": {"example": p2(example), "input": p2()},
    }


if __name__ == "__main__":
    fire.Fire()
