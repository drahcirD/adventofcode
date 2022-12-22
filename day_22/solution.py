#! /usr/bin/env python
import pathlib
import fire
import collections
import itertools
import numpy as np


def e1(path=pathlib.Path(__file__).resolve().parent / "example.txt"):
    return p1(path)


def e2(path=pathlib.Path(__file__).resolve().parent / "example.txt"):
    return p2(path)


def print_room(room):

    for y in range(1, max(room, key=lambda x: x[1])[1]):
        for x in range(1, max(room, key=lambda x: x[0])[0]):
            try:
                print(room[(x,y)], end='')
            except:
                pass
        print()

def p1(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        map_in, way = [x for x in path.read_text().split("\n\n")]
        graph = {}
        for i, row in enumerate(map_in.split("\n"), 1):
            for j, col in enumerate(row, 1):
                graph[(j,i)] = col

        instructions = []
        start = 0
        for i, c in enumerate(way):
            try:
                int(c)
            except ValueError:
                instructions.append(int(way[start:i]))
                instructions.append(c)
                start = i + 1
        print_room(graph)
        return graph, instructions

    def solve(graph, instructions):
        pathway = graph.copy()
        cur = (1, 1)
        while graph[cur] == " ":
            cur = (cur[0] + 1, 1)
        start = cur
        direction = (1, 0)
        for instr in instructions:
            print(f"{instr=}")
            if isinstance(instr, str):
                match direction:
                    case (1, 0):
                        if instr == "R":
                            direction = (0, 1)
                        else:
                            direction = (0, -1)
                    case (-1, 0):
                        if instr == "R":
                            direction = (0, -1)
                        else:
                            direction = (0, 1)
                    case (0, 1):
                        if instr == "R":
                            direction = (-1, 0)
                        else:
                            direction = (1, 0)
                    case (0, -1):
                        if instr == "R":
                            direction = (1, 0)
                        else:
                            direction = (-1, 0)
                print(f"{direction=}")
            else:
                for i in range(instr):
                    match direction:
                        case (1, 0):
                             pathway[cur] = '>'
                        case (-1, 0):
                            pathway[cur] = '<'
                        case (0, 1):
                            pathway[cur] = 'v'
                        case (0, -1):
                            pathway[cur] = '^'
                    print(f"{cur=}")
                    new = (cur[0] + direction[0], cur[1] + direction[1])
                    match graph.get(new, None):
                        case ".":
                            cur = new
                        case "#":
                            break
                        case " ":
                            new2=new
                            while graph.get(new2, None) == " ":
                                new = new2
                                new2 = (new[0] + direction[0], new[1] + direction[1])
                            match graph.get(new2, None):
                                case ".":
                                    cur = new
                                case "#":
                                    break
                                case None:
                                    match direction:
                                        case (1, 0):
                                            new = min(
                                                (
                                                    k
                                                    for k, v in graph.items()
                                                    if v != " " and k[1] == cur[1]
                                                ),
                                                key=lambda k: k[0],
                                            )
                                        case (-1, 0):
                                            new = max(
                                                (
                                                    k
                                                    for k, v in graph.items()
                                                    if v != " " and k[1] == cur[1]
                                                ),
                                                key=lambda k: k[0],
                                            )
                                        case (0, 1):
                                            new = min(
                                                (
                                                    k
                                                    for k, v in graph.items()
                                                    if v != " " and k[0] == cur[0]
                                                ),
                                                key=lambda k: k[1],
                                            )
                                        case (0, -1):
                                            new = max(
                                                (
                                                    k
                                                    for k, v in graph.items()
                                                    if v != " " and k[0] == cur[0]
                                                ),
                                                key=lambda k: k[1],
                                            )
                                    if graph[new] == '#':
                                        break
                                    cur = new
                        case None:
                            match direction:
                                case (1, 0):
                                    new = min(
                                        (
                                            k
                                            for k, v in graph.items()
                                            if v != " " and k[1] == cur[1]
                                        ),
                                        key=lambda k: k[0],
                                    )
                                case (-1, 0):
                                    new = max(
                                        (
                                            k
                                            for k, v in graph.items()
                                            if v != " " and k[1] == cur[1]
                                        ),
                                        key=lambda k: k[0],
                                    )
                                case (0, 1):
                                    new = min(
                                        (
                                            k
                                            for k, v in graph.items()
                                            if v != " " and k[0] == cur[0]
                                        ),
                                        key=lambda k: k[1],
                                    )
                                case (0, -1):
                                    new = max(
                                        (
                                            k
                                            for k, v in graph.items()
                                            if v != " " and k[0] == cur[0]
                                        ),
                                        key=lambda k: k[1],
                                    )
                            if graph[new] == '#':
                                break
                            cur = new
        
        col_offset = min(
                    (
                        k
                        for k, v in graph.items()
                        if v != " " and k[1] == cur[1]
                    ),
                    key=lambda k: k[1],
                )[0]
        col = cur[0]-col_offset+1
        # row_offset = min(
        #             (
        #                 k
        #                 for k, v in graph.items()
        #                 if v != " " and k[1] == cur[1]
        #             ),
        #             key=lambda k: k[1],
        #         )[0]
        row = cur[1]
        print(col_offset)
        print(col,row)
        # print_room(pathway)
        match direction:
            case (1, 0):
                return 1000*row+4*col
            case (-1, 0):
                return 1000*row+4*col+2
            case (0, 1):
                return 1000*row+4*col+1
            case (0, -1):
                return 1000*row+4*col+3
    return solve(*parse())


def p2(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        return []

    def solve(data):
        pass

    return solve(parse())


def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": p1(example), "input": p1()},
        "part2": {"example": p2(example), "input": p2()},
    }


if __name__ == "__main__":
    fire.Fire()
