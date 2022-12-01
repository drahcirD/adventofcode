#! /usr/bin/env python
import pathlib
import numpy as np
from typing import Tuple
import fire
import numba


@numba.njit()
def manhattan(p1: Tuple[int, int], p2: Tuple[int, int]):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def p1(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [
            x.replace(",", "").replace(":", "").split(" ")
            for x in path.read_text().split("\n")
        ]
        data = []
        for line in lines:
            data.append(
                (
                    int(line[2].split("=")[1]),
                    int(line[3].split("=")[1]),
                    int(line[-2].split("=")[1]),
                    int(line[-1].split("=")[-1]),
                )
            )
        return data

    def solve(data):
        line = 2000000
        beacons = set()
        sensors = []
        for sx, sy, bx, by in data:
            dist = manhattan((sx, sy), (bx, by))
            beacons.add((bx, by))
            sensors.append((sx, sy, dist))

        min_x = min([x - dist for x, y, dist in sensors])
        max_x = max([x + dist for x, y, dist in sensors])

        @numba.njit()
        def find(min_x, max_x, beacons, sensors):
            size = 0
            for i in range(min_x, max_x + 1):
                for sx, sy, dist in sensors:
                    if manhattan((sx, sy), (i, line)) <= dist and (i, line) not in beacons:
                        size += 1
                        break
            return size
        return find(min_x, max_x, beacons, np.array(sensors))

    return solve(parse())


def p2(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [
            x.replace(",", "").replace(":", "").split(" ")
            for x in path.read_text().split("\n")
        ]
        data = []
        for line in lines:
            data.append(
                (
                    int(line[2].split("=")[1]),
                    int(line[3].split("=")[1]),
                    int(line[-2].split("=")[1]),
                    int(line[-1].split("=")[-1]),
                )
            )
        return np.array(data)

    def solve(data):
        @numba.njit(nogil=True)
        def setup(data):
            max_pos = 4000000
            positions = set()
            for sx, sy, bx, by in data:
                dist = manhattan((sx, sy), (bx, by)) + 1
                for x in range(max(sx - dist, 0), min(sx + dist, max_pos) + 1):
                    y = sy + dist - abs(sx - x)
                    y2 = sy - dist + abs(sx - x)
                    if 0 <= y <= max_pos:
                        positions.add((x, y))
                    if 0 <= y2 <= max_pos:
                        positions.add((x, y2))
            return positions

        @numba.njit(nogil=True)
        def find(positions, sensors):
            for x, y in positions:
                bad = False
                for sx, sy, dist in sensors:
                    if manhattan((sx, sy), (x, y)) <= dist:
                        bad = True
                        break
                if not bad:
                    return x * 4000000 + y

        return find(
            setup(data),
            [(sx, sy, manhattan((sx, sy), (bx, by))) for sx, sy, bx, by in data],
        )

    return solve(parse())


def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": p1(example), "input": p1()},
        "part2": {"example": p2(example), "input": p2()},
    }


if __name__ == "__main__":
    fire.Fire()
