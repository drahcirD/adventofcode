#! /usr/bin/env python
import math
import pathlib
from pprint import pprint
import fire
import collections
import itertools
import more_itertools
import numpy as np
import sympy

from aocd import data as aoc_data
from aocd import submit


def parse(data):
    lines = [x for x in data.split("\n\n")]
    return lines


def p1(data=aoc_data):
    data = parse(data)

    result = 0
    # Button A: X+94, Y+34
    # Button B: X+22, Y+67
    # Prize: X=8400, Y=5400
    for d in data:
        a, b, p = d.split("\n")
        _, _, ax, ay = a.split(" ")
        ax = int(ax[2:].rstrip(","))
        ay = int(ay[2:].rstrip(","))
        _, _, bx, by = b.split(" ")
        bx = int(bx[2:].rstrip(","))
        by = int(by[2:].rstrip(","))
        _, px, py = p.split(" ")
        px = int(px[2:].rstrip(","))
        py = int(py[2:].rstrip(","))
        min_cost = float("inf")
        for i in range(101):
            for j in range(101):
                if i * ax + j * bx == px and i * ay + j * by == py:
                    cost = 3 * i + j
                    if cost < min_cost:
                        min_cost = cost
        result += min_cost if min_cost < float("inf") else 0

    return result


def parse2(data):
    return parse(data)


def p2(data=aoc_data):
    data = parse2(data)

    result = 0
    # Button A: X+94, Y+34
    # Button B: X+22, Y+67
    # Prize: X=8400, Y=5400
    for d in data:
        a, b, p = d.split("\n")
        _, _, ax, ay = a.split(" ")
        ax = int(ax[2:].rstrip(","))
        ay = int(ay[2:].rstrip(","))
        _, _, bx, by = b.split(" ")
        bx = int(bx[2:].rstrip(","))
        by = int(by[2:].rstrip(","))
        _, px, py = p.split(" ")
        px = int(px[2:].rstrip(",")) + 10000000000000
        py = int(py[2:].rstrip(",")) + 10000000000000

        A = np.array([[ax, bx], [ay, by]])
        y = np.array([px, py])
        x = np.linalg.inv(A) @ y

        i, j = x
        if abs(round(i) - i) < 0.001 and abs(round(j) - j) < 0.001:
            cost = 3 * round(i) + round(j)
            result += int(cost)

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
