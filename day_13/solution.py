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

DAY = '13'
DEBUG = False

def parse_input(lines: List[str]):
    dots = {}
    commands = []
    for line in lines:
        if ',' in line:
            dot = tuple(map(int, line.split(',')))
            dots[dot] = True
        elif line.startswith('fold along'):
            m = re.search(r'([xy])=(\d+)', line)
            cmd = m[1], int(m[2])
            commands.append(cmd)
        elif line:
            raise ValueError(f"Unrecognized line format: {line}")
    validate(dots, commands)
    return dots, commands


def validate(dots, commands):
    """Sanity check"""

    maxx = max(cmd[1] for cmd in commands if cmd[0] == 'x') * 2
    maxy = max(cmd[1] for cmd in commands if cmd[0] == 'y') * 2
    # print(maxx, maxy)

    for x, y in dots.keys():
        if x > maxx or y > maxy:
            msg = "Shit: {} is outside of {}".format((x,y), (maxx, maxy))
            # print(msg)
            raise ValueError(msg)


def print_board(dots):
    maxx = max([d[0] for d in dots])
    maxy = max([d[1] for d in dots])

    print(f"dimensions (h,v): {(maxx, maxy)}")

    board = ''
    for y in range(1+maxy):
        for x in range(1+maxx):
            dot = (x,y)
            sign = "#" if dot in dots else "."
            board += sign
        board += '\n'

    print(board)


def fold(dots: list, cmd: tuple):
    axis, at = cmd
    # print(axis, at)
    # print(dots)
    newdots = {}

    if axis == 'x': # fold left
        for x, y in dots.keys():
            if x > at:
                x = at - (x - at)
            newdots[(x, y)] = True

    if axis == 'y': # fold up
        for x, y in dots.keys():
            if y > at:
                y = at - (y - at)
            newdots[(x, y)] = True
    # print(len(newdots))
    return newdots


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    dots, commands = parse_input(lines)
    # print_board(dots)
    for cmd in commands:
        dots = fold(dots, cmd)
        # print_board(dots)
        break
    
    return len(dots)


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    dots, commands = parse_input(lines)
    for cmd in commands:
        dots = fold(dots, cmd)
        # print_board(dots)
    print_board(dots) # PZEHRAER
    return len(dots)



tests = [
    (utils.load_input('test.1.txt'), 17, 16),
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
    exp1 = 814
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = 108
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
