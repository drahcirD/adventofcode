#! /usr/bin/env python
import pathlib
import fire
import collections
import itertools

def sign(n):
    if n > 0:
        return 1
    elif n < 0:
        return -1
    else:
        return 0

def p1(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [x.split(" ") for x in path.read_text().split("\n")]
        return lines

    def solve(data):
        head, tail = (0, 0), (0, 0)
        tail_positions = set((0, 0))
        way = []
        for moves in data:
            move = int(moves[1])
            print(moves[0])
            for i in range(move):
                if moves[0] == "R":
                    head = (head[0] + 1, head[1])
                elif moves[0] == "L":
                    head = (head[0] - 1, head[1])
                elif moves[0] == "U":
                    head = (head[0], head[1] + 1)
                elif moves[0] == "D":
                    head = (head[0], head[1] - 1)
                x_diff = head[0] - tail[0]
                y_diff = head[1] - tail[1]

                if abs(x_diff) == 2 and abs(y_diff) == 0:
                    tail = (tail[0] + sign(x_diff), tail[1])
                elif abs(x_diff) == 0 and abs(y_diff) == 2:
                    tail = (tail[0], tail[1] + sign(y_diff))
                elif abs(x_diff) == 1 and abs(y_diff) == 1:
                    pass
                elif not (
                    (abs(x_diff) == 1 and abs(y_diff) == 0)
                    or (abs(x_diff) == 0 and abs(y_diff) == 1)
                ):
                    tail = (tail[0] + sign(x_diff), tail[1] + sign(y_diff))
                if tail not in tail_positions:
                    way.append(tail)
                tail_positions.add(tail)
                print(head, tail)
        print(tail_positions)
        return len(way)

    return solve(parse())


def p2(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [x.split(" ") for x in path.read_text().split("\n")]
        return lines

    def solve(data):
        head = (0, 0)
        tails = [(0, 0) for _ in range(9)]
        tail_positions = set()
        tail_positions.add((0,0))
        way = []
        for moves in data:
            move = int(moves[1])
            print(moves[0])
            for i in range(move):
                if moves[0] == "R":
                    head = (head[0] + 1, head[1])
                elif moves[0] == "L":
                    head = (head[0] - 1, head[1])
                elif moves[0] == "U":
                    head = (head[0], head[1] + 1)
                elif moves[0] == "D":
                    head = (head[0], head[1] - 1)
                cur_head = head
                for j, tail in enumerate(tails[:-1]):
                    x_diff = cur_head[0] - tail[0]
                    y_diff = cur_head[1] - tail[1]

                    if abs(x_diff) == 2 and abs(y_diff) == 0:
                        tails[j] = (tail[0] + sign(x_diff), tail[1])
                    elif abs(x_diff) == 0 and abs(y_diff) == 2:
                        tails[j] = (tail[0], tail[1] + sign(y_diff))
                    elif abs(x_diff) == 1 and abs(y_diff) == 1:
                        pass
                    elif not (
                        (abs(x_diff) == 1 and abs(y_diff) == 0)
                        or (abs(x_diff) == 0 and abs(y_diff) == 1)
                    ):
                        tails[j] = (tail[0] + sign(x_diff), tail[1] + sign(y_diff))
                    cur_head = tail
                x_diff = cur_head[0] - tails[-1][0]
                y_diff = cur_head[1] - tails[-1][1]
                tail = tails[-1]
                if abs(x_diff) == 2 and abs(y_diff) == 0:
                    tails[-1] = (tail[0] + sign(x_diff), tail[1])
                elif abs(x_diff) == 0 and abs(y_diff) == 2:
                    tails[-1] = (tail[0], tail[1] + sign(y_diff))
                elif abs(x_diff) == 1 and abs(y_diff) == 1:
                    pass
                elif not (
                    (abs(x_diff) == 1 and abs(y_diff) == 0)
                    or (abs(x_diff) == 0 and abs(y_diff) == 1)
                ):
                    tails[-1] = (tail[0] + sign(x_diff), tail[1] + sign(y_diff))
                if tail[-1] not in tail_positions:
                    way.append(tails[-1])
                tail_positions.add(tails[-1])
                print(cur_head, tails[-1])
        cur_head = head
        for k in range(100):
            for j, tail in enumerate(tails[:-1]):
                x_diff = cur_head[0] - tail[0]
                y_diff = cur_head[1] - tail[1]

                if abs(x_diff) == 2 and abs(y_diff) == 0:
                    tails[j] = (tail[0] + sign(x_diff), tail[1])
                elif abs(x_diff) == 0 and abs(y_diff) == 2:
                    tails[j] = (tail[0], tail[1] + sign(y_diff))
                elif abs(x_diff) == 1 and abs(y_diff) == 1:
                    pass
                elif not (
                    (abs(x_diff) == 1 and abs(y_diff) == 0)
                    or (abs(x_diff) == 0 and abs(y_diff) == 1)
                ):
                    tails[j] = (tail[0] + sign(x_diff), tail[1] + sign(y_diff))
                cur_head = tail
            x_diff = cur_head[0] - tails[-1][0]
            y_diff = cur_head[1] - tails[-1][1]
            tail = tails[-1]
            if abs(x_diff) == 2 and abs(y_diff) == 0:
                tails[-1] = (tail[0] + sign(x_diff), tail[1])
            elif abs(x_diff) == 0 and abs(y_diff) == 2:
                tails[-1] = (tail[0], tail[1] + sign(y_diff))
            elif abs(x_diff) == 1 and abs(y_diff) == 1:
                pass
            elif not (
                (abs(x_diff) == 1 and abs(y_diff) == 0)
                or (abs(x_diff) == 0 and abs(y_diff) == 1)
            ):
                tails[-1] = (tail[0] + sign(x_diff), tail[1] + sign(y_diff))
            if tail[-1] not in tail_positions:
                way.append(tails[-1])
            tail_positions.add(tails[-1])
            print(cur_head, tails[-1])
            print(tail_positions)
            print(head,tails)

        return len(tail_positions)

    return solve(parse())


def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    example2 = pathlib.Path(__file__).resolve().parent / "example2.txt"
    return {
        "part1": {"example": p1(example), "input": p1()},
        "part2": {"example": p2(example), "example2": p2(example2), "input": p2()},
    }


if __name__ == "__main__":
    fire.Fire()
