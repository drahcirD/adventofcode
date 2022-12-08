#! /usr/bin/env python
import pathlib
import fire


def p1(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [[int(y) for y in x.strip()] for x in path.read_text().split("\n")]
        return lines

    def solve(data):
        n_visible = len(data) * 2 + len(data[0]) * 2 - 4
        visible = set()
        for row in range(1, len(data) - 1):
            limit = data[row][0]
            for col in range(1, len(data[0]) - 1):
                if data[row][col] > limit:
                    if (row, col) not in visible:
                        n_visible += 1
                        visible.add((row, col))
                    limit = data[row][col]

        for row in range(1, len(data) - 1):
            limit = data[row][-1]
            for col in reversed(range(1, len(data[0]) - 1)):
                if data[row][col] > limit:
                    if (row, col) not in visible:
                        n_visible += 1
                        visible.add((row, col))
                    limit = data[row][col]

        for col in range(1, len(data[0]) - 1):
            limit = data[-1][col]
            for row in reversed(range(1, len(data) - 1)):
                if data[row][col] > limit:
                    if (row, col) not in visible:
                        n_visible += 1
                        visible.add((row, col))
                    limit = data[row][col]

        for col in range(1, len(data[0]) - 1):
            limit = data[0][col]
            for row in range(1, len(data) - 1):
                if data[row][col] > limit:
                    if (row, col) not in visible:
                        n_visible += 1
                        visible.add((row, col))
                    limit = data[row][col]

        return n_visible

    return solve(parse())


def p2(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [[int(y) for y in x.strip()] for x in path.read_text().split("\n")]
        return lines

    def solve(data):
        max_score = -1
        for row in range(1, len(data[0]) - 1):
            for col in range(1, len(data) - 1):
                score = 1
                for direction in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
                    n = 0
                    index = (row + direction[0], col + direction[1])
                    while (
                        0 <= index[0] < len(data)
                        and 0 <= index[1] < len(data[0])
                        and data[index[0]][index[1]] <= data[row][col]
                    ):
                        n += 1
                        index = (index[0] + direction[0], index[1] + direction[1])
                    
                    if not (0 <= index[0] < len(data) and 0 <= index[1] < len(data[0])):
                        n -= 1

                    score *= n
                if score > max_score:
                    max_score = score
        return max_score

    return solve(parse())


def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": p1(example), "input": p1()},
        "part2": {"example": p2(example), "input": p2()},
    }


if __name__ == "__main__":
    fire.Fire()
