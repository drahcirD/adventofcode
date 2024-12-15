#! /usr/bin/env python
import functools
import operator
import pathlib
from pprint import pprint
import fire
import collections
import itertools
import more_itertools
import numpy as np

from aocd import data as aoc_data
from aocd import submit


def parse(data):
    map, moves = data.split("\n\n")
    arr = np.array([np.asarray([x for x in row]) for row in map.split("\n")])
    moves = functools.reduce(operator.iadd, moves.split("\n"), [])
    return arr, moves


def print_room(room):
    height, width = room.shape
    for r in range(height):
        for c in range(width):
            print(room[r, c], end="")
        print()


def p1(data=aoc_data):
    map, moves = parse(data)

    result = 0

    width, height = map.shape
    start = None
    for r in range(height):
        for c in range(width):
            if map[r, c] == "@":
                start = (r, c)
                break
        if start:
            break

    cur = start
    for m in moves:
        r, c = cur

        match m:
            case ">":
                c += 1
            case "<":
                c -= 1
            case "v":
                r += 1
            case "^":
                r -= 1
        if map[r, c] == "#":
            continue

        if map[r, c] == "O":
            i = 1
            r2, c2 = None, None
            match m:
                case ">":
                    r2, c2 = r, c + i
                    while map[r2, c2] == "O":
                        r2, c2 = r, c + i
                        i += 1
                case "<":
                    r2, c2 = r, c - i
                    while map[r2, c2] == "O":
                        r2, c2 = r, c - i
                        i += 1
                case "v":
                    r2, c2 = r + i, c
                    while map[r2, c2] == "O":
                        r2, c2 = r + i, c
                        i += 1
                case "^":
                    r2, c2 = r - i, c
                    while map[r2, c2] == "O":
                        r2, c2 = r - i, c
                        i += 1
            assert r2 is not None and c2 is not None
            if map[r2, c2] == "#":
                continue
            map[r2, c2] = map[r, c]

        map[r, c] = "@"
        map[cur] = "."
        cur = r, c
        # print(m)
        # print_room(map)

    for r in range(height):
        for c in range(width):
            if map[r, c] == "O":
                result += 100 * r + c
    return result


def parse2(data):
    return parse(data)


def p2(data=aoc_data):
    map, moves = parse2(data)
    result = 0
    height, width = map.shape
    new_map = np.zeros((height, width * 2), dtype="<U1")
    start = None
    for r in range(height):
        for c in range(width):
            if map[r, c] == "@":
                start = (r, c * 2)
                new_map[start] = "@"
                new_map[r, c * 2 + 1] = "."
            elif map[r, c] == "#":
                new_map[r, c * 2] = "#"
                new_map[r, c * 2 + 1] = "#"
            elif map[r, c] == "O":
                new_map[r, c * 2] = "["
                new_map[r, c * 2 + 1] = "]"
            else:
                new_map[r, c * 2] = "."
                new_map[r, c * 2 + 1] = "."
    map = new_map
    height, width = map.shape

    print_room(map)

    cur = start
    for m in moves:
        r, c = cur

        match m:
            case ">":
                c += 1
            case "<":
                c -= 1
            case "v":
                r += 1
            case "^":
                r -= 1
        if map[r, c] == "#":
            continue

        if map[r, c] in {"[", "]"}:
            cur_positions = {(r, c)}

            if map[r, c] == "[":
                cur_positions.add((r, c + 1))
            else:
                cur_positions.add((r, c - 1))

            new_positions = set()
            positions = cur_positions
            while cur_positions:
                for pos in cur_positions:
                    r3, c3 = pos
                    to_add = None
                    match m:
                        case ">":
                            if map[r3, c3 + 1] in {"[", "]"}:
                                to_add = (r3, c3 + 1)
                        case "<":
                            if map[r3, c3 - 1] in {"[", "]"}:
                                to_add = (r3, c3 - 1)
                        case "v":
                            if map[r3 + 1, c3] in {"[", "]"}:
                                to_add = (r3 + 1, c3)
                        case "^":
                            if map[r3 - 1, c3] in {"[", "]"}:
                                to_add = (r3 - 1, c3)
                    if (
                        to_add
                        and to_add not in positions
                        and to_add not in cur_positions
                    ):
                        new_positions.add(to_add)
                        r3, c3 = to_add
                        if map[to_add] == "[":
                            new_positions.add((r3, c3 + 1))
                        else:
                            new_positions.add((r3, c3 - 1))

                positions.update(new_positions)
                cur_positions = new_positions
                new_positions = set()

            can_move = True
            for pos in positions:
                r3, c3 = pos
                match m:
                    case ">":
                        if map[r3, c3 + 1] == "#":
                            can_move = False
                            break
                    case "<":
                        if map[r3, c3 - 1] == "#":
                            can_move = False
                            break
                    case "v":
                        if map[r3 + 1, c3] == "#":
                            can_move = False
                            break
                    case "^":
                        if map[r3 - 1, c3] == "#":
                            can_move = False
                            break

            if not can_move:
                continue
            ordered_positions = list(positions)
            match m:
                case ">":
                    ordered_positions = sorted(
                        ordered_positions, key=operator.itemgetter(1), reverse=True
                    )
                case "<":
                    ordered_positions = sorted(
                        ordered_positions, key=operator.itemgetter(1)
                    )
                case "v":
                    ordered_positions = sorted(
                        ordered_positions, key=operator.itemgetter(0), reverse=True
                    )
                case "^":
                    ordered_positions = sorted(
                        ordered_positions, key=operator.itemgetter(0)
                    )

            for pos in ordered_positions:
                r3, c3 = pos
                match m:
                    case ">":
                        map[r3, c3 + 1], map[pos] = map[pos], map[r3, c3 + 1]
                    case "<":
                        map[r3, c3 - 1], map[pos] = map[pos], map[r3, c3 - 1]
                    case "v":
                        map[r3 + 1, c3], map[pos] = map[pos], map[r3 + 1, c3]
                    case "^":
                        map[r3 - 1, c3], map[pos] = map[pos], map[r3 - 1, c3]

        map[r, c] = "@"
        map[cur] = "."
        cur = r, c
        # print(m)
        # print_room(map)

    print_room(map)

    for r in range(height):
        for c in range(width):
            if map[r, c] == "[":
                result += 100 * r + c
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


def e2(path=pathlib.Path(__file__).resolve().parent / "example3.txt"):
    return p2(path.read_text())


if __name__ == "__main__":
    fire.Fire()
