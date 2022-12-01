#! /usr/bin/env python
import pathlib
from queue import PriorityQueue
import sys
import fire

def dijkstra(data, start, end):
    distances = {}
    distances[start] = 0

    visited = set()
    pq = PriorityQueue()
    pq.put((0, start))

    while not pq.empty():
        (cur_dist, cur) = pq.get()
        if cur == end:
            return distances
        visited.add(cur)
        r,c = cur
        neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        for neighbor in neighbors:
            if neighbor not in data:
                continue
            if neighbor in visited:	
                continue
            if data[neighbor] - data[cur] > 1:
                continue

            old_path_cost = distances.get(neighbor, sys.maxsize)
            new_path_cost = cur_dist + 1
            if new_path_cost < old_path_cost:
                pq.put((new_path_cost, neighbor))
                distances[neighbor] = new_path_cost
    return distances

def p1(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = {
            (x, y): ord(vy)
            for x, vx in enumerate(path.read_text().split("\n"))
            for y, vy in enumerate(vx)
        }
        return lines

    def solve(data):
        start_marker = ord("S")
        start = None
        end_marker = ord("E")
        end = None
        for coord, val in data.items():
            if val == start_marker:
                start = coord
                data[coord] = ord('a')
            elif val == end_marker:
                end = coord
                data[coord] = ord('z')
            if start and end:
                break

        return dijkstra(data, start, end)[end]
    return solve(parse())


def p2(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = {
            (x, y): ord(vy)
            for x, vx in enumerate(path.read_text().split("\n"))
            for y, vy in enumerate(vx)
        }
        return lines

    def solve(data):
        starts = []
        end_marker = ord("E")
        end = None
        for coord, val in data.items():
            if val == ord('a'):
                starts.append(coord)
            elif val == end_marker:
                end = coord
                data[coord] = ord('z')
        
        return min([dijkstra(data, start, end).get(end, sys.maxsize) for start in starts])

    return solve(parse())


def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": p1(example), "input": p1()},
        "part2": {"example": p2(example), "input": p2()},
    }


if __name__ == "__main__":
    fire.Fire()
