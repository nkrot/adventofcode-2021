#!/usr/bin/env python

# # #
#
#

import os
import sys

from typing import List, Tuple, Union
from functools import reduce

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '10'
DEBUG = False

SCORES = {
    ")": (3, 1),
    "]": (57, 2),
    "}": (1197, 3),
    ">": (25137, 4)
}

BRACKETS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">"
}


class Stack(object):

    def __init__(self):
        self.items = []

    def push(self, val):
        self.items.insert(0, val)

    def pop(self):
        return self.items.pop(0)

    def __len__(self):
        return len(self.items)

    def __str__(self):
        return "".join(self.items)


def analyse(record: str) -> Union[Tuple[int, str], Stack]:
    """Return either the 1st non-balanced symbol as Tuple[idx, symbol] or
    the whole stack after traversing record. If the record is complete,
    returned stack will be empty, otherwise it will contain a sequence of
    characters necessary to complement the record.
    """
    st = Stack()
    for idx, ch in enumerate(record):
        # print(idx, ch)
        if ch in BRACKETS:
            st.push(BRACKETS[ch])
        else:
            exp = st.pop()
            if exp != ch:
                return (idx, ch)
    return st


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    score = 0
    for line in lines:
        res = analyse(line)
        if isinstance(res, tuple):
            score += SCORES[res[1]][0]
    return score


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    scores = []
    for line in lines:
        res = analyse(line)
        if isinstance(res, Stack) and res:
            score = reduce(lambda a, b: a*5+SCORES[b][1], res.items, 0)
            # print(res, score)
            scores.append(score)

    scores.sort()

    return scores[int(len(scores) / 2)]


tests = [
    (utils.load_input('test.1.txt'), 6+57+1197+25137, 288957),
    (["<{([{{}}[<[[[<>{}]]]>[]]"], 0, 294),
    (["[({(<(())[]>[[{[]{<()<>>"], 0, 288957)
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
    exp1 = 442131
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = 3646451424
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
