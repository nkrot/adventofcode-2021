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
from day_09.solution import Board

DAY = '11'
DEBUG = False

Board.AROUND.extend([(-1, -1), (-1, +1), (+1, -1), (+1, +1)])
assert len(set(Board.AROUND)) == 8,  "Wrong number of neighbor coordinates"


def flash_octopus(octopuses: Board, current, flashed_octopuses):

    pos, energy = current

    if energy < 10 or pos in flashed_octopuses:
        return 0

    if DEBUG:
        print("Flashes", current)

    # current octopus flashes and gets discharged
    octopuses[pos] = 0
    c_flashed = 1

    flashed_octopuses.append(pos)

    # flashing charges neighboring octopuses
    for neigh in octopuses.neighbors_of(pos):
        if neigh[0] not in flashed_octopuses:
            octopuses[neigh[0]] += 1

    # some neighbors can also flash
    for neigh in octopuses.neighbors_of(pos):
        if neigh[0] in flashed_octopuses:
            continue
        if neigh[1] > 9:
            c_flashed += flash_octopus(octopuses, neigh, flashed_octopuses)

    return c_flashed


def tick(octopuses: Board):
    """one moment in time"""
    c_flashes = 0

    # update all by 1
    for coord, energy in octopuses:
        octopuses[coord] += 1

    if DEBUG:
        print("--- after + 1 ---")
        print(octopuses)

    flashed = []
    for octo in octopuses:
        c_flashes += flash_octopus(octopuses, octo, flashed)

    return c_flashes


def solve_p1(lines: List[str], steps=1) -> int:
    """Solution to the 1st part of the challenge"""
    cavern = Board.from_lines(lines)
    if DEBUG:
        print("--- Before ---")
        print(cavern)
        print()

    c_flashes = 0
    for t in range(steps):
        c_flashes += tick(cavern)
        if DEBUG:
            print(f"---- after {1+t} ---")
            print(cavern)
            print()

    return c_flashes


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    # TODO
    return 0


text_1 = """11111
19991
19191
19991
11111\
"""


tests = [
    ((text_1.split('\n'), 2), 9, None),
    ((utils.load_input('test.2.txt'), 10), 204, None),
    ((utils.load_input('test.2.txt'), 100), 1656, None)
]


def run_tests():
    print("--- Tests ---")

    for tid, (inp, exp1, exp2) in enumerate(tests):
        if exp1 is not None:
            res1 = solve_p1(*inp)
            print(f"T1.{tid}:", res1 == exp1, exp1, res1)

        if exp2 is not None:
            res2 = solve_p2(inp)
            print(f"T2.{tid}:", res2 == exp2, exp2, res2)


def run_real():
    lines = utils.load_input()

    print(f"--- Day {DAY} p.1 ---")
    exp1 = 1729
    res1 = solve_p1(lines, 100)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = -1
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
