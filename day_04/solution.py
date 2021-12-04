#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '04'
DEBUG = False


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


def parse_input(lines: List[str]):
    lines.append('')
    numbers, boards = [], []
    rows = []
    for idx, line in enumerate(lines):
        if idx == 0:
            numbers = utils.to_numbers(line.split(','))
        elif line:
            rows.append(line)
        elif rows:
            board = BingoBoard.from_lines(rows)
            boards.append(board)
            board.id = len(boards)
            rows = []
    return numbers, boards


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    random_order, boards = parse_input(lines)
    for draw in random_order:
        for board in boards:
            if board.mark(draw) and board.wins():
                score = board.score(draw)
                return score
    return 0


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    random_order, boards = parse_input(lines)
    finished_boards = [False] * len(boards)
    score = 0
    for draw in random_order:
        for idx, board in enumerate(boards):
            if finished_boards[idx]:
                continue
            if board.mark(draw) and board.wins():
                score = board.score(draw)
                # print("Board {} wins at {} with score {}".format(
                #     board.id, draw, score))
                finished_boards[idx] = (board, score)
    return score


text_1 = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""


tests = [
    (text_1.split('\n'), 188 * 24, 148 * 13),
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
