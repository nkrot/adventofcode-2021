#!/usr/bin/env python

# # #
#
#

import os
import sys
from typing import List, Tuple

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '04'
DEBUG = not False


class BingoBoard(object):

    @classmethod
    def from_lines(cls, rows: List[str]):
        numbers = [utils.to_numbers(row.split()) for row in rows]
        return cls(numbers)

    def __init__(self, rows):
        self.rows = rows
        self.width = len(rows[0])

    def mark(self, target: int) -> bool:
        """If given number <target> is present on the board, mark it as found
        and return True. If not found, return False.
        """
        finds = 0
        for items in self.rows:
            if target in items:
                idx = items.index(target)
                items[idx] = str(items[idx])
                finds += 1
        return bool(finds)

    def wins(self) -> bool:
        """The board wins if there is at least one complete row or column of
        marked numbers."""
        for row in self.rows:
            if all(isinstance(n, str) for n in row):
                return True
        for idx in range(self.width):
            column = [row[idx] for row in self.rows]
            if all(isinstance(n, str) for n in column):
                return True
        return False

    def score(self, k: int) -> int:
        """The score is a sum of all unmarked numbers multiplied by given
        coefficient <k>."""
        s = 0
        for row in self.rows:
            s += sum(n for n in row if not isinstance(n, str))
        return s * k


def parse_input(lines: List[str]) -> Tuple[List[int], List['BingoBoard']]:
    lines.append('')
    numbers, boards = [], []
    rows = []
    for idx, line in enumerate(lines):
        if idx == 0:
            numbers = utils.to_numbers(line.split(','))
        elif line:
            rows.append(line)
        elif rows:
            boards.append(BingoBoard.from_lines(rows))
            rows = []
    for idx, board in enumerate(boards):
        board.id = idx + 1
    return numbers, boards


def solve_p1(lines: List[str], part=1) -> int:
    """Solution to the 1st and the 2nd parts of the challenge"""
    random_order, boards = parse_input(lines)
    finished_boards = [False] * len(boards)
    score = 0
    for draw in random_order:
        for idx, board in enumerate(boards):
            if finished_boards[idx]:
                continue
            if board.mark(draw) and board.wins():
                score = board.score(draw)
                finished_boards[idx] = (board, score)
                if DEBUG:
                    print("Board {} wins at {} with score {}".format(
                        board.id, draw, score))
                if part == 1:
                    return score
    return score


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    return solve_p1(lines, 2)


tests = [
    (utils.load_input('test.1.txt'), 188 * 24, 148 * 13),
]


def run_tests():
    print("--- Tests ---")

    for tid, (inp, exp1, exp2) in enumerate(tests):
        if exp1 is not None:
            res1 = solve_p1(inp)
            print(f"T1.{tid}:", res1 == exp1, exp1, res1)

        if exp2 is not None:
            res2 = solve_p2(inp)
            print(f"T2.{tid}:", res2 == exp2, exp2, res2)


def run_real():
    lines = utils.load_input()

    print(f"--- Day {DAY} p.1 ---")
    exp1 = 29440
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = 13884
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
