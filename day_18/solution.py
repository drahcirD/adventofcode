#! /usr/bin/env python
from functools import lru_cache
import sys
import operator
import pathlib
import sys
import fire
import itertools
import tqdm


def p1(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [[int(y) for y in x.split(",")] for x in path.read_text().split("\n")]
        return lines

    def solve(data):
        cubes = {(x, y, z): 6 for x, y, z in data}
        for cube1, cube2 in itertools.combinations(cubes, r=2):
            if (
                abs(cube1[0] - cube2[0])
                + abs(cube1[1] - cube2[1])
                + abs(cube1[2] - cube2[2])
                == 1
            ):
                cubes[cube1] -= 1
                cubes[cube2] -= 1
        return sum(cubes.values())

    return solve(parse())


def p2(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [
            tuple([int(y) for y in x.split(",")]) for x in path.read_text().split("\n")
        ]
        return lines

    def solve(cubes):
        max_x = max(cubes, key=operator.itemgetter(0))[0]
        max_y = max(cubes, key=operator.itemgetter(1))[1]
        max_z = max(cubes, key=operator.itemgetter(2))[2]
        min_x = min(cubes, key=operator.itemgetter(0))[0]
        min_y = min(cubes, key=operator.itemgetter(1))[1]
        min_z = min(cubes, key=operator.itemgetter(2))[2]
        airs = set(
            [
                (x, y, z)
                for x in range(min_x - 1, max_x + 1)
                for y in range(min_y - 1, max_y + 1)
                for z in range(min_z - 1, max_z + 1)
            ]
        )
        airs -= set(cubes)
        cube_set = set(cubes)

        sys.setrecursionlimit(10000)

        @lru_cache()
        def can_escape(index):
            if index in cube_set or index in visited:
                return False
            x, y, z = index
            visited.add(index)
            if (
                x > max_x + 1
                or y > max_y + 1
                or z > max_z + 1
                or x < min_x - 1
                or y < min_y - 1
                or z < min_z - 1
            ):
                return True

            return any(
                can_escape(index)
                for index in [
                    (x - 1, y, z),
                    (x + 1, y, z),
                    (x, y - 1, z),
                    (x, y + 1, z),
                    (x, y, z - 1),
                    (x, y, z + 1),
                ]
            )

        for air in tqdm.tqdm(airs.copy()):
            visited = set()
            if can_escape(air):
                airs.remove(air)

        cubes = {(x, y, z): 6 for x, y, z in cubes}
        for cube1, cube2 in itertools.combinations(cubes, r=2):
            if (
                abs(cube1[0] - cube2[0])
                + abs(cube1[1] - cube2[1])
                + abs(cube1[2] - cube2[2])
                == 1
            ):
                cubes[cube1] -= 1
                cubes[cube2] -= 1

        for cube in cubes:
            for air in airs:
                if (
                    abs(cube[0] - air[0])
                    + abs(cube[1] - air[1])
                    + abs(cube[2] - air[2])
                    == 1
                ):
                    cubes[cube] -= 1

        return sum(cubes.values())

    return solve(parse())


def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": p1(example), "input": p1()},
        "part2": {"example": p2(example), "input": p2()},
    }


if __name__ == "__main__":
    fire.Fire()
