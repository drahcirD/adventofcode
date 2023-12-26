#! /usr/bin/env python
import pathlib
from pprint import pprint

import tqdm
import fire
import collections
import itertools
import more_itertools
import numpy as np
import sympy
from sympy import Line, Point

from aocd import data as aoc_data
from aocd import submit


def parse(data):
    lines = [x for x in data.split("\n")]
    return lines


def p1(data=aoc_data):
    data = parse(data)

    result = 0
    hails = []
    for d in data:
        pos, vel = d.split(" @ ")
        pos = [int(x) for x in pos.split(", ")]
        vel = [int(x) for x in vel.split(", ")]
        hail1 = (pos, vel)
        start = Point(hail1[0][0], hail1[0][1])
        line = Line(
            Point(hail1[0][0], hail1[0][1]),
            Point(hail1[0][0] + hail1[1][0], hail1[0][1] + hail1[1][1]),
        )
        hails.append((start, vel, line))

    min_limit = 200000000000000
    max_limit = 400000000000000

    for hail1, hail2 in tqdm.tqdm(list(itertools.combinations(hails, r=2))):
        start1, vel1, line1 = hail1
        start2, vel2, line2 = hail2

        for intersect in line1.intersect(line2):
            if (vel1[0] > 0 and intersect.x < start1.x) or (
                vel1[0] < 0 and intersect.x > start1.x
            ):
                continue
            if (vel1[1] > 0 and intersect.y < start1.y) or (
                vel1[1] < 0 and intersect.y > start1.y
            ):
                continue

            if (vel2[0] > 0 and intersect.x < start2.x) or (
                vel2[0] < 0 and intersect.x > start2.x
            ):
                continue
            if (vel2[1] > 0 and intersect.y < start2.y) or (
                vel2[1] < 0 and intersect.y > start2.y
            ):
                continue

            if (min_limit <= intersect.x <= max_limit) and (
                min_limit <= intersect.y <= max_limit
            ):
                result += 1

    return result


def parse2(data):
    return parse(data)


def p2(data=aoc_data):
    data = parse2(data)
    result = 0
    hails = []
    (
        stone_x,
        stone_y,
        stone_z,
        stone_xs,
        stone_ys,
        stone_zs,
    ) = sympy.symbols("stone_x stone_y stone_z stone_xs stone_ys stone_zs")
    for d in data:
        pos, vel = d.split(" @ ")
        pos = [int(x) for x in pos.split(", ")]
        vel = [int(x) for x in vel.split(", ")]
        hail = (pos, vel)
        hails.append(hail)

    equations = []

    symbols = [stone_x, stone_y, stone_z, stone_xs, stone_ys, stone_zs]
    for i, (pos, vel) in enumerate(hails):
        var = sympy.symbols(f"t{i}")
        symbols.append(var)
        equations.extend(
            [
                sympy.Eq(vel[0] * var + pos[0], stone_xs * var + stone_x),
                sympy.Eq(vel[1] * var + pos[1], stone_ys * var + stone_y),
                sympy.Eq(vel[2] * var + pos[2], stone_zs * var + stone_z),
            ]
        )
        if len(equations) > len(symbols):
            break

    result = sympy.solve(equations, tuple(symbols))
    print(result)
    return sum(result[0][:3])


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
