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

DAY = '21'
DEBUG = int(os.environ.get('DEBUG', 0))


class DeterministicDie(object):

    def __init__(self):
        self.min = 1
        self.max = 100
        self.value = 0
        self.times = 0

    def __next__(self):
        self.value += 1
        self.times += 1
        if self.value > self.max:
            self.value = 1
        return self.value


def test_dice():
    die = DeterministicDie()
    for _ in range(101):
        v = next(die)
        print(v)


def make_one_move(pos, score, die, player):
    moves = [next(die) for _ in range(3)]
    pos += sum(moves)
    pos = pos % 10 if pos % 10 else 10
    score += pos
    if DEBUG:
        print("Player", player, moves, pos, score)
    return pos, score


def play(p1, p2, die, min_wining_score = 1000):

    p1_score, p2_score = 0, 0

    while True:
        p1, p1_score = make_one_move(p1, p1_score, die, 1)
        if p1_score >= min_wining_score:
            return die.times * p2_score

        p2, p2_score = make_one_move(p2, p2_score, die, 2)
        if p2_score >= min_wining_score:
            return die.times * p1_score


def solve_p1(p1, p2) -> int:
    """Solution to the 1st part of the challenge"""
    die = DeterministicDie()
    return play(p1, p2, die, 1000)


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    # TODO
    return 0


tests = [
    ((4, 8), 745 * 993, 444356092776315)
]


def run_tests():
    print("--- Tests ---")

    for tid, (inp, exp1, exp2) in enumerate(tests):
        if exp1 is not None:
            res1 = solve_p1(*inp)
            print(f"T.{tid}.p1:", res1 == exp1, exp1, res1)

        if exp2 is not None:
            res2 = solve_p2(inp)
            print(f"T.{tid}.p2:", res2 == exp2, exp2, res2)


def run_real():
    lines = utils.load_input()

    print(f"--- Day {DAY} p.1 ---")
    exp1 = 679329
    res1 = solve_p1(7, 9)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = -1
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
