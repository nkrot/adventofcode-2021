#!/usr/bin/env python

# # #
#
#

import os
import sys
from typing import List
from collections import Counter

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DAY = '03'
DEBUG = False


def count_bits(lines: List[str]):
    return [Counter(ln[i] for ln in lines) for i in range(len(lines[0]))]


def count_bits_at(lines: List[str], idx: int):
    return Counter(ln[idx] for ln in lines)


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    gamma, epsilon = '', ''
    for bits in count_bits(lines):
        most, least = bits.most_common(2)  # ties are possible
        gamma += most[0]
        epsilon += least[0]
    return int(gamma, 2) * int(epsilon, 2)


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""

    def select(numbers: List[str], selector) -> str:
        numbers = list(numbers)
        for idx in range(len(numbers[0])):
            target = selector(count_bits_at(numbers, idx))
            numbers = [num for num in numbers if num[idx] == target]
            if len(numbers) == 1:
                break
        return numbers.pop(0)

    def most_frequent(counts: Counter) -> str:
        most, least = counts.most_common(2)
        return '1' if most[1] == least[1] else most[0]

    def least_frequent(counts: Counter) -> str:
        most, least = counts.most_common(2)
        return '0' if most[1] == least[1] else least[0]

    ox = select(lines, most_frequent)
    co2 = select(lines, least_frequent)

    return int(ox, 2) * int(co2, 2)


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
