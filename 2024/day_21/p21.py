#! /usr/bin/env python
import functools
import math
import pathlib
from pprint import pprint
import fire
import collections
import itertools
import more_itertools
import numpy as np

from aocd import data as aoc_data
from aocd import submit
from tqdm import tqdm


def parse(data):
    lines = [x for x in data.split("\n")]
    return lines


def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def dir_to_move(r, c):
    match r, c:
        case (1, 0):
            return "v"
        case (-1, 0):
            return "^"
        case (0, 1):
            return ">"
        case (0, -1):
            return "<"
    assert False, f"({r},{c})"


def mover(r, c, nbr, map):
    rn, cn = np.where(map == nbr)
    rn, cn = rn[0], cn[0]
    moves = []

    rbad, cbad = np.where(map == "-1")
    rbad, cbad == rbad[0], cbad[0]
    dir_c = np.sign(cn - c)

    if dir_c > 0 and (rn, c) != (rbad, cbad):
        go_horiz = False
    elif (r, cn) != (rbad, cbad):
        go_horiz = True
    elif (rn, c) != (rbad, cbad):
        go_horiz = False
    else:
        assert False

    if go_horiz:
        while c != cn:
            dir_c = np.sign(cn - c)

            if dir_c != 0 and 0 <= c + dir_c < map.shape[1] and map[r, c + dir_c] != "-1":
                c += dir_c
                moves.append(dir_to_move(0, dir_c))

        while r != rn:
            dir_r = np.sign(rn - r)

            if dir_r != 0 and 0 <= r + dir_r < map.shape[0] and map[r + dir_r, c] != "-1":
                r += dir_r
                moves.append(dir_to_move(dir_r, 0))
    else:
        while r != rn:
            dir_r = np.sign(rn - r)

            if dir_r != 0 and 0 <= r + dir_r < map.shape[0] and map[r + dir_r, c] != "-1":
                r += dir_r
                moves.append(dir_to_move(dir_r, 0))

        while c != cn:
            dir_c = np.sign(cn - c)

            if dir_c != 0 and 0 <= c + dir_c < map.shape[1] and map[r, c + dir_c] != "-1":
                c += dir_c
                moves.append(dir_to_move(0, dir_c))
    moves.append("A")

    return moves, r, c


def p1(data=aoc_data):
    data = parse(data)

    result = 0

    keypad = np.array([[7, 8, 9], [4, 5, 6], [1, 2, 3], [-1, 0, "A"]])
    dirpad = np.array(
        [
            [-1, "^", "A"],
            ["<", "v", ">"],
        ]
    )

    for d in data:
        keypad_moves = []
        r, c = 3, 2
        for nbr in d:
            new_moves, r, c = mover(r, c, nbr, keypad)
            keypad_moves.extend(new_moves)

        dirpad_moves1 = []
        r, c = 0, 2
        for move in keypad_moves:
            new_moves, r, c = mover(r, c, move, dirpad)
            dirpad_moves1.extend(new_moves)

        dirpad_moves2 = []
        r, c = 0, 2
        for move in dirpad_moves1:
            new_moves, r, c = mover(r, c, move, dirpad)
            dirpad_moves2.extend(new_moves)

        result += int(d[:-1]) * len(dirpad_moves2)
    return result


def parse2(data):
    return parse(data)


def mover2(r, c, rn, cn, rbad, cbad):
    dir_r = rn - r
    dir_c = cn - c

    if dir_c > 0 and (rn, c) != (rbad, cbad):
        vertical_first = True
    elif (r, cn) != (rbad, cbad):
        vertical_first = False
    elif (rn, c) != (rbad, cbad):
        vertical_first = True
    else:
        assert False

    horiz = ">" if dir_c > 0 else "<"
    horiz *= abs(cn - c)
    vert = "v" if dir_r > 0 else "^"
    vert *= abs(rn - r)
    if vertical_first:
        return f"{vert}{horiz}A"
    else:
        return f"{horiz}{vert}A"


def p2(data=aoc_data):
    data = parse2(data)

    result = 0

    keypad = np.array([[7, 8, 9], [4, 5, 6], [1, 2, 3], [-1, 0, "A"]])
    dirpad = np.array(
        [
            [-1, "^", "A"],
            ["<", "v", ">"],
        ]
    )
    keypad_map = {}
    dirpad_map = {}

    for r in range(keypad.shape[0]):
        for c in range(keypad.shape[1]):
            keypad_map[keypad[r, c]] = (r, c)

    for r in range(dirpad.shape[0]):
        for c in range(dirpad.shape[1]):
            dirpad_map[dirpad[r, c]] = (r, c)

    for d in data:
        keypad_moves = ""
        r, c = 3, 2

        rbad, cbad = keypad_map["-1"]
        for nbr in d:
            rn, cn = keypad_map[nbr]
            new_moves = mover2(r, c, rn, cn, rbad, cbad)
            keypad_moves += new_moves
            r, c = rn, cn

        last_moves = collections.Counter({keypad_moves: 1})
        rbad, cbad = dirpad_map["-1"]
        for i in range(26):
            dirpad_moves = collections.Counter()
            r, c = 0, 2
            for move, n in last_moves.items():
                for step in move:
                    rn, cn = dirpad_map[step]
                    new_moves = mover2(r, c, rn, cn, rbad, cbad)
                    dirpad_moves[new_moves] += n
                    r, c = rn, cn

            last_moves = dirpad_moves
        result += int(d[:-1]) * sum(last_moves.values())
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
