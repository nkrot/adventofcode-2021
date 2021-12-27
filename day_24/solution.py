#!/usr/bin/env python

# # #
#
# Use genetic algorithm for finding model numbers that are valid
# https://www.reddit.com/r/adventofcode/comments/rnwnvb/2021_day_24_musings_on_ways_to_approach_this_and/
#
# in the input:
# there are 14 read instructions.
# are there 14 independent blocks? what do they do? are each responsible for
# a digit in the input?

import re
import os
import sys
from typing import List, Dict, Union

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '24'
DEBUG = int(os.environ.get('DEBUG', 0))


class Monad(object):

    @classmethod
    def from_lines(cls, lines: List[str]):
        instructions = []
        for line in lines:
            if line:
                inst, *ops = line.split()
                assert len(ops) in {1,2}, f"Wrong line length: {line}"

                if inst == 'div':
                    inst = "__floordiv__"
                else:
                    inst = f"__{inst}__"

                if len(ops) == 2 and re.match(r'-?\d+', ops[1]):
                        ops[1] = int(ops[1])
                elif len(ops) == 1:
                    ops.append(None)

                instructions.append((inst, *ops))
        return cls(instructions)

    def __init__(self, instructions):
        self.instructions: list = instructions
        self.registers: Dict[str, int] = self._defaults()

    def _defaults(self):
        return {'w': 0, 'x': 0, 'y': 0, 'z': 0}

    def exec(self, inputs: List[int]):
        # inputs = list(map(int, list(inputs)))
        self.registers = self._defaults()
        for inst, op1, op2 in self.instructions:
            if isinstance(op2, str):
                op2 = self.registers[op2]
            if inst == '__inp__':
                self.registers[op1] = inputs.pop(0)
            elif inst == '__eql__':
                self.registers[op1] = int(self.registers[op1] == op2)
            else:
                self.registers[op1] = getattr(self.registers[op1], inst)(op2)

    def is_valid(self, modelno: Union[str,List[int]]):
        inputs = list(map(int, list(modelno)))
        length = len(inputs)
        assert length == 14, f"Wrong model number length: 14 vs {length}"
        self.exec(inputs)
        return self.registers['z'] == 0


def model_numbers(length=14):
    """Generate all possible valid model numbers"""
    digits = list(reversed(range(1, 10)))
    def generate(length):
        if length == 1:
            for d in digits:
                yield [d]
        else:
            for head in digits:
                for tail in generate(length-1):
                    yield [head, *tail]
    yield from generate(length)


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    m = {True: 'valid', False: 'Invalid'}
    monad = Monad.from_lines(lines)
    i = 0
    for modelno in model_numbers():
        i += 1
        valid = monad.is_valid(modelno)
        if DEBUG > 0 or not(i % 1000000):
            print("{}\t{}\t{}".format(
                "".join(map(str, modelno)), m[valid], monad.registers['z']))
        if valid:
            break
    print(modelno)
    return 0


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    # TODO
    return 0


tests = [
    (utils.load_input('test.1.txt'), 1, None),
    # TODO
]


def run_tests():
    print("--- Tests ---")

    for tid, (inp, exp1, exp2) in enumerate(tests):
        if exp1 is not None:
            res1 = solve_p1(inp)
            print(f"T.{tid}.p1:", res1 == exp1, exp1, res1)

        if exp2 is not None:
            res2 = solve_p2(inp)
            print(f"T.{tid}.p2:", res2 == exp2, exp2, res2)


def run_real():
    lines = utils.load_input()

    print(f"--- Day {DAY} p.1 ---")
    exp1 = -1
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = -1
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
