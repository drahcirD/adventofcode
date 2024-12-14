#! /usr/bin/env python
import functools
import operator
import pathlib
from pprint import pprint
from time import sleep
import fire
import collections
import itertools
import more_itertools
import numpy as np

from aocd import data as aoc_data
from aocd import submit


def parse(data):
    lines = [x for x in data.split("\n")]
    return lines


def p1(data=aoc_data):
    data = parse(data)

    if len(data) == 12:
        maxx = 11
        maxy = 7
    else:
        maxx = 101
        maxy = 103

    robots = []
    for d in data:
        p, v = d.split(" ")
        p = p[2:].split(",")
        x, y = int(p[0]), int(p[1].rstrip())
        v = v[2:].split(",")
        vx, vy = int(v[0]), int(v[1].rstrip())
        robots.append([x, y, vx, vy])
    for i in range(100):
        for r in robots:
            r[0] = (r[0] + r[2]) % maxx
            r[1] = (r[1] + r[3]) % maxy

    quadrants = [0, 0, 0, 0]

    for r in robots:
        x, y = r[:2]
        if x < maxx // 2 and y < maxy // 2:
            quadrants[0] += 1
        elif x > maxx // 2 and y < maxy // 2:
            quadrants[1] += 1
        elif x < maxx // 2 and y > maxy // 2:
            quadrants[2] += 1
        elif x > maxx // 2 and y > maxy // 2:
            quadrants[3] += 1

    return functools.reduce(operator.mul, quadrants, 1)


def parse2(data):
    return parse(data)


def print_room(robots, maxx, maxy):
    for y in range(maxy):
        for x in range(maxx):
            if (x, y) in robots:
                print(robots[(x, y)], end="")
            else:
                print(".", end="")
        print()


def p2(data=aoc_data):
    data = parse2(data)

    if len(data) == 12:
        maxx = 11
        maxy = 7
    else:
        maxx = 101
        maxy = 103

    robots = []
    for d in data:
        p, v = d.split(" ")
        p = p[2:].split(",")
        x, y = int(p[0]), int(p[1].rstrip())
        v = v[2:].split(",")
        vx, vy = int(v[0]), int(v[1].rstrip())
        robots.append([x, y, vx, vy])
    n = 1
    while True:
        cur_map = collections.Counter()
        for r in robots:
            r[0] = (r[0] + r[2]) % maxx
            r[1] = (r[1] + r[3]) % maxy
            cur_map[tuple(r[:2])] += 1

        # print all rooms, find one interesting and look at all modulo room size until a pretty picture appears...
        # in my case the first interesting was at n=86 and the pretty picture at 7055
        if (n - 86) % 101 == 0:
            print(n)
            print_room(cur_map, maxx, maxy)
            sleep(0.5)
        n += 1


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
