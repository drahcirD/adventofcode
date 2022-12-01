#! /usr/bin/env python
import functools
import pathlib
import fire
import collections
import itertools

import enum


class RETURNVALUE(enum.Enum):
    OK = enum.auto()
    NOK = enum.auto()
    CONT = enum.auto()


def check(left, right):
    ret = RETURNVALUE.OK
    for j, lval in enumerate(left):
        try:
            rval = right[j]
        except IndexError:
            ret = RETURNVALUE.NOK
            break

        if isinstance(lval, int) and isinstance(rval, int):
            if lval > rval:
                ret = RETURNVALUE.NOK
                break
            elif lval < rval:
                ret = RETURNVALUE.OK
                break
        elif isinstance(lval, list) and isinstance(rval, list):
            match check(lval, rval):
                case RETURNVALUE.NOK:
                    ret = RETURNVALUE.NOK
                    break
                case RETURNVALUE.OK:
                    ret = RETURNVALUE.OK
                    break
        elif isinstance(lval, list):
            match check(lval, [rval]):
                case RETURNVALUE.NOK:
                    ret = RETURNVALUE.NOK
                    break
                case RETURNVALUE.OK:
                    ret = RETURNVALUE.OK
                    break
        elif isinstance(rval, list):
            match check([lval], rval):
                case RETURNVALUE.NOK:
                    ret = RETURNVALUE.NOK
                    break
                case RETURNVALUE.OK:
                    ret = RETURNVALUE.OK
                    break
    else:
        if len(left) == len(right):
            ret = RETURNVALUE.CONT

    return ret


def p1(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [x.split("\n") for x in path.read_text().split("\n\n")]
        pairs = []
        for left, right in lines:
            lval = eval(left)
            rval = eval(right)
            pairs.append([lval, rval])
        return pairs

    def solve(data):
        indices = []
        for i, (left, right) in enumerate(data, 1):
            ret = check(left, right)
            if ret == RETURNVALUE.OK:
                indices.append(i)

        return sum(indices)

    return solve(parse())


def p2(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [x.split("\n") for x in path.read_text().split("\n\n")]
        packets = []
        for left, right in lines:
            lval = eval(left)
            rval = eval(right)
            packets.append(lval)
            packets.append(rval)
        return packets

    def solve(data):
        def cmp(left, right):
            match check(left, right):
                case RETURNVALUE.NOK:
                    return 1
                case RETURNVALUE.OK:
                    return -1

        a = [[2]]
        b = [[6]]
        data.append(a)
        data.append(b)
        sort = sorted(data, key=functools.cmp_to_key(cmp))

        return (sort.index(a) + 1) * (sort.index(b) + 1)

    return solve(parse())


def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": p1(example), "input": p1()},
        "part2": {"example": p2(example), "input": p2()},
    }


if __name__ == "__main__":
    fire.Fire()
