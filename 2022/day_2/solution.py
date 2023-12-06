#! /usr/bin/env python
import pathlib
import fire

single_scores = {"X": 1, "Y": 2, "Z": 3}
scores = {
    "X": {"A": 3, "B": 0, "C": 6},
    "Y": {"A": 6, "B": 3, "C": 0},
    "Z": {"A": 0, "B": 6, "C": 3},
}


def p1(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [x.split(" ") for x in path.read_text().split("\n")]
        return lines

    def solve(data):
        score = 0
        for they, me in data:
            score += single_scores[me] + scores[me][they]

        return score

    return solve(parse())


def p2(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [x.split(" ") for x in path.read_text().split("\n")]
        return lines

    def solve(data):
        choice = {
            "X": {"A": "Z", "B": "X", "C": "Y"},
            "Y": {"A": "X", "B": "Y", "C": "Z"},
            "Z": {"A": "Y", "B": "Z", "C": "X"},
        }
        score = 0
        for they, result in data:
            me = choice[result][they]
            score += single_scores[me] + scores[me][they]

        return score

    return solve(parse())


def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": p1(example), "input": p1()},
        "part2": {"example": p2(example), "input": p2()},
    }


if __name__ == "__main__":
    fire.Fire()
