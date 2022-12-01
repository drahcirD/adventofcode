#! /usr/bin/env python
import pathlib
import fire
import collections


def e1(path=pathlib.Path(__file__).resolve().parent / "example.txt"):
    return p1(path)


def e2(path=pathlib.Path(__file__).resolve().parent / "example.txt"):
    return p2(path)


def print_room(room):

    for y in range(max(room, key=lambda x: x[1])[1] + 1):
        for x in range(max(room, key=lambda x: x[0])[0] + 1):
            try:
                print(room[(x, y)], end="")
            except:
                print(" ", end="")
        print()


def p1(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        map_in, way = [x for x in path.read_text().split("\n\n")]
        graph = {}
        for i, row in enumerate(map_in.split("\n")):
            for j, col in enumerate(row):
                if col == " ":
                    continue
                graph[(j, i)] = col

        instructions = []
        start = 0
        for i, c in enumerate(way):
            try:
                int(c)
            except ValueError:
                instructions.append(int(way[start:i]))
                instructions.append(c)
                start = i + 1
        instructions.append(int(way[start:]))
        return graph, instructions

    def solve(graph, instructions):
        pathway = graph.copy()
        cur = min(
            (k for k, v in graph.items() if v == "." and k[1] == 0),
            key=lambda k: k[0],
        )
        direction = (1, 0)
        for instr in instructions:
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
            else:
                for _ in range(instr):
                    match direction:
                        case (1, 0):
                            pathway[cur] = ">"
                        case (-1, 0):
                            pathway[cur] = "<"
                        case (0, 1):
                            pathway[cur] = "v"
                        case (0, -1):
                            pathway[cur] = "^"
                    new = (cur[0] + direction[0], cur[1] + direction[1])
                    match graph.get(new, None):
                        case ".":
                            cur = new
                        case "#":
                            continue
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
                            if graph[new] == "#":
                                break
                            cur = new
                        case _:
                            assert False

        col = cur[0] + 1
        row = cur[1] + 1
        match direction:
            case (1, 0):
                return 1000 * row + 4 * col
            case (-1, 0):
                return 1000 * row + 4 * col + 2
            case (0, 1):
                return 1000 * row + 4 * col + 1
            case (0, -1):
                return 1000 * row + 4 * col + 3

    return solve(*parse())


def p2(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        map_in, way = [x for x in path.read_text().split("\n\n")]
        graph = collections.defaultdict(dict)
        face_index = {}
        sub_index = collections.defaultdict(int)
        count = 1
        if len(map_in) < 200:
            size = 4
        else:
            size = 50
        for i, row in enumerate(map_in.split("\n")):
            offset = 0
            for j, col in enumerate(row):
                if col == " ":
                    offset += 1
                    continue
                try:
                    face_index[(j // size, i // size)]
                except:
                    face_index[(j // size, i // size)] = count
                    count += 1

                sub = sub_index[face_index[(j // size, i // size)]]
                graph[face_index[(j // size, i // size)]][
                    (sub % size, sub // size)
                ] = col
                sub_index[face_index[(j // size, i // size)]] += 1
        

        instructions = []
        start = 0
        for i, c in enumerate(way):
            try:
                int(c)
            except ValueError:
                instructions.append(int(way[start:i]))
                instructions.append(c)
                start = i + 1
        instructions.append(int(way[start:]))
        return dict(graph), instructions

    def solve(graph, instructions):
        if len(graph[1]) == 16:
            size = 4
        elif len(graph[1]) == 2500:
            size = 50
        else:
            assert False
        if size ==4:
            # not solved for example
            return -1
        cur_face = 1
        cur_pos = (0, 0)
        direction = (1, 0)
        for instr in instructions:
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
            else:
                for _ in range(instr):
                    new = (cur_pos[0] + direction[0], cur_pos[1] + direction[1])
                    match graph[cur_face].get(new, None):
                        case ".":
                            cur_pos = new
                        case "#":
                            break
                        case None:
                            match direction:
                                case (1, 0):
                                    match cur_face:
                                        case 1:
                                            new_face = 2
                                            new_pos = (0, cur_pos[1])
                                            new_direction = direction
                                        case 2:
                                            new_face = 5
                                            new_pos = (
                                                size - 1,
                                                size - cur_pos[1] - 1,
                                            )
                                            new_direction = (-1,0)
                                        case 3:
                                            new_face = 2
                                            new_pos = (cur_pos[1], size - 1)
                                            new_direction = (0,-1)
                                        case 4:
                                            new_face = 5
                                            new_pos = (0, cur_pos[1])
                                            new_direction = direction
                                        case 5:
                                            new_face = 2
                                            new_pos = (
                                                size - 1,
                                                size - cur_pos[1] - 1,
                                            )
                                            new_direction = (-1,0)
                                        case 6:
                                            new_face = 5
                                            new_pos = (
                                                cur_pos[1],
                                                size - 1,
                                            )
                                            new_direction = (0,-1) 
                                        case _:
                                            assert False
                                case (-1, 0):
                                    match cur_face:
                                        case 1:
                                            new_face = 4
                                            new_pos = (0, size - cur_pos[1] - 1)
                                            new_direction = (1,0)
                                        case 2:
                                            new_face = 1
                                            new_pos = (size - 1, cur_pos[1])
                                            new_direction = direction
                                        case 3:
                                            new_face = 4
                                            new_pos = (cur_pos[1], 0)
                                            new_direction = (0,1)
                                        case 4:
                                            new_face = 1
                                            new_pos = (0, size - cur_pos[1] - 1)
                                            new_direction = (1,0)
                                        case 5:
                                            new_face = 4
                                            new_pos = (size - 1, cur_pos[1])
                                            new_direction = direction
                                        case 6:
                                            new_face = 1
                                            new_pos = (cur_pos[1], 0)
                                            new_direction = (0,1)
                                        case _:
                                            assert False
                                case (0, 1):
                                    match cur_face:
                                        case 1:
                                            new_face = 3
                                            new_pos = (cur_pos[0], 0)
                                            new_direction = direction
                                        case 2:
                                            new_face = 3
                                            new_pos = (size - 1, cur_pos[0])
                                            new_direction = (-1,0)
                                        case 3:
                                            new_face = 5
                                            new_pos = (cur_pos[0], 0)
                                            new_direction = direction
                                        case 4:
                                            new_face = 6
                                            new_pos = (cur_pos[0], 0)
                                            new_direction = direction
                                        case 5:
                                            new_face = 6
                                            new_pos = (size - 1, cur_pos[0])
                                            new_direction = (-1,0)
                                        case 6:
                                            new_face = 2
                                            new_pos = (cur_pos[0], 0)
                                            new_direction = direction
                                        case _:
                                            assert False
                                case (0, -1):
                                    match cur_face:
                                        case 1:
                                            new_face = 6
                                            new_pos = (0, cur_pos[0])
                                            new_direction = (1,0)
                                        case 2:
                                            new_face = 6
                                            new_pos = (cur_pos[0], size - 1)
                                            new_direction = direction
                                        case 3:
                                            new_face = 1
                                            new_pos = (cur_pos[0], size - 1)
                                            new_direction = direction
                                        case 4:
                                            new_face = 3
                                            new_pos = (0, cur_pos[0])
                                            new_direction = (1,0)
                                        case 5:
                                            new_face = 3
                                            new_pos = (cur_pos[0], size - 1)
                                            new_direction = direction
                                        case 6:
                                            new_face = 4
                                            new_pos = (cur_pos[0], size - 1)
                                            new_direction = direction
                                        case _:
                                            assert False
                                case _:
                                    assert False

                            if graph[new_face][new_pos] == "#":
                                break
                            cur_pos = new_pos
                            cur_face = new_face
                            direction = new_direction
                        case _:
                            assert False


        match cur_face:
            case 1:
                r = cur_pos[1]
                c = cur_pos[0]+50
            case 2:
                r = cur_pos[1]
                c = cur_pos[0] + 100
            case 3:
                r = cur_pos[1]+50
                c = cur_pos[0]+50
            case 4:
                r = cur_pos[1]+100
                c = cur_pos[0]
            case 5:
                r = cur_pos[1]+100
                c = cur_pos[0]+50
            case 6:
                r = cur_pos[1]+150
                c = cur_pos[0]
            case _:
                assert False

        match direction:
            case (1, 0):
                return 1000 * (r+1) + 4 * (c+1)
            case (-1, 0):
                return 1000 * (r+1) + 4 * (c+1) + 2
            case (0, 1):
                return 1000 * (r+1) + 4 *  (c+1) + 1
            case (0, -1):
                return 1000 * (r+1) + 4 *  (c+1) + 3

    return solve(*parse())


def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": p1(example), "input": p1()},
        "part2": {"example": p2(example), "input": p2()},
    }


if __name__ == "__main__":
    fire.Fire()
