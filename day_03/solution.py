#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List
from collections import Counter

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DAY = '03'  # TODO
DEBUG = False


def count_bits(lines: List[str]):
    return [Counter(ln[i] for ln in lines) for i in range(len(lines[0]))]


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    gamma, epsilon = '', ''
    for bits in count_bits(lines):
        g, e = bits.most_common(2)
        gamma += g[0]
        epsilon += e[0]
    gr = int(gamma, 2)
    er = int(epsilon, 2)
    return gr * er


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    ox_numbers = list(lines)
    co2_numbers = list(lines)

    for idx in range(len(lines[0])):
        bits = count_bits(ox_numbers)
        most, least = bits[idx].most_common(2)
        target = '1' if most[1] == least[1] else most[0]
        ox_numbers = [num for num in ox_numbers if num[idx] == target]
        # print(ox_numbers)
        if len(ox_numbers) == 1:
            break
    # print(ox_numbers)

    for idx in range(len(lines[0])):
        bits = count_bits(co2_numbers)
        most, least = bits[idx].most_common(2)
        target = '0' if most[1] == least[1] else least[0]
        co2_numbers = [num for num in co2_numbers if num[idx] == target]
        # print(co2_numbers)
        if len(co2_numbers) == 1:
            break
    # print(co2_numbers)

    oxr = int(ox_numbers[0], 2)
    co2r = int(co2_numbers[0], 2)
    return oxr * co2r


text_1 = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""


tests = [
    (text_1.split('\n'), 22*9, 23*10),
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
    exp1 = 1082324
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = 1353024
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
