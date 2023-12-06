#! /usr/bin/env python
import operator
import pathlib
import fire
import collections
import itertools

ROCK = 1
SAND = 2


def p1(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [x.replace("-> ", "").split(" ") for x in path.read_text().split("\n")]
        room = {}
        for line in lines:
            for p1, p2 in itertools.pairwise(line):
                x1, y1 = [int(k) for k in p1.split(",")]
                x2, y2 = [int(k) for k in p2.split(",")]

                if x2 < x1:
                    x1, x2 = x2, x1

                if y2 < y1:
                    y1, y2 = y2, y1
                for x in range(x1, x2 + 1):
                    room[(x, y1)] = ROCK

                for y in range(y1, y2 + 1):
                    room[(x1, y)] = ROCK
        return room

    def solve(data):
        start = (500, 0)
        MAX_FALLS = 1e4
        sand = start
        falls = 0
        while falls < MAX_FALLS:
            falls += 1
            if (sand[0], sand[1] + 1) not in data:
                sand = (sand[0], sand[1] + 1)
            elif (sand[0] - 1, sand[1] + 1) not in data:
                sand = (sand[0] - 1, sand[1] + 1)
            elif (sand[0] + 1, sand[1] + 1) not in data:
                sand = (sand[0] + 1, sand[1] + 1)
            elif sand != start:
                data[sand] = SAND
                sand = start
                falls = 0

        return len([sand for sand in data.values() if sand == SAND])

    return solve(parse())


def p2(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [x.replace("-> ", "").split(" ") for x in path.read_text().split("\n")]
        room = {}
        for line in lines:
            for p1, p2 in itertools.pairwise(line):
                x1, y1 = [int(k) for k in p1.split(",")]
                x2, y2 = [int(k) for k in p2.split(",")]

                if x2 < x1:
                    x1, x2 = x2, x1

                if y2 < y1:
                    y1, y2 = y2, y1
                for x in range(x1, x2 + 1):
                    room[(x, y1)] = ROCK

                for y in range(y1, y2 + 1):
                    room[(x1, y)] = ROCK
        y_max = max(room, key=operator.itemgetter(1))
        for x in range(int(-1e4), int(1e4)):
            room[x, 2 + y_max[1]] = ROCK

        return room

    def solve(data):
        start = (500, 0)
        sand = start
        falls = 0
        while start not in data:
            falls += 1
            if (sand[0], sand[1] + 1) not in data:
                sand = (sand[0], sand[1] + 1)
            elif (sand[0] - 1, sand[1] + 1) not in data:
                sand = (sand[0] - 1, sand[1] + 1)
            elif (sand[0] + 1, sand[1] + 1) not in data:
                sand = (sand[0] + 1, sand[1] + 1)
            else:
                data[sand] = SAND
                sand = start
                falls = 0

        return len([sand for sand in data.values() if sand == SAND])

    return solve(parse())


def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": p1(example), "input": p1()},
        "part2": {"example": p2(example), "input": p2()},
    }


if __name__ == "__main__":
    fire.Fire()
