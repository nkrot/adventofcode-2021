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


def analyse(record: str) -> Tuple[str, Stack]:
    """Check the record for balance of brackets and return a tuple of two:
    1) the 1st imbalanced character if the record is corrupted or None if
       the record is balanced (= not corrupted)
    2) the stack after traversing the whole record. If the record is complete,
       the stack will be empty. If the record is incomplete and not corrupted,
       the stack will contain characters necessary to complement the record.
    """
    bad = None
    st = Stack()
    for idx, ch in enumerate(record):
        # print(idx, ch)
        if ch in BRACKETS:
            st.push(BRACKETS[ch])
        else:
            exp = st.pop()
            if exp != ch:
                bad = ch
                break
    return bad, st


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    score = 0
    for line in lines:
        imbalanced, _ = analyse(line)
        if imbalanced:
            score += SCORES[imbalanced][0]
    return score


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    scores = []
    for line in lines:
        imbalanced, st = analyse(line)
        if not imbalanced and st:
            score = reduce(lambda a, b: a*5+SCORES[b][1], st.items, 0)
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
