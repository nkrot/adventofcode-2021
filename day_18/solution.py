#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List, Union
from functools import total_ordering
from itertools import combinations

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '18'
DEBUG = int(os.environ.get('DEBUG', 0))


tests = [
    (utils.load_input('test.1.txt'), 4140, 3993),
]


class SNError(Exception):
    pass


@total_ordering
class RN(object):
    """Regular value, behaves like int

    TODO: make it similar to SN and add start/end? this can help simplify
    SN.from_string()
    """

    def __init__(self, value):
        self.value = int(value)
        self.parent = None
        self.position = None  # among siblings

    def __int__(self):
        return int(self.value)

    def __len__(self):
        return len(str(self))

    def __str__(self):
        return str(self.value)

    def __lt__(self, other):
        other = other.value if isinstance(other, type(self)) else other
        return self.value < other

    def __eq__(self, other):
        other = other.value if isinstance(other, type(self)) else other
        return self.value == other

    def __iadd__(self, other):
        assert isinstance(other, type(self)), \
            f"Unsuported object type: {type(other)}"
        self.value += other.value

    def __repr__(self):
        return "<{}: value={} position={} parent={}>".format(
            self.__class__.__name__, self.value, self.position, self.parent)

    @property
    def magnitude(self):
        return self.value

    @property
    def level(self):
        return 1 + (self.parent.level if self.parent else 0)

    def split(self):
        left = self.__class__(self.value // 2)
        right = self.__class__((self.value + 1) // 2)
        sn = SN(left, right)
        return sn

    def is_sibling(self, other):
        return self.parent == other.parent


class SN(object):
    """Snailfish Number"""

    # This is used in testing only
    ALLOW_LONG_NUMBERS = False

    @staticmethod
    def sum(numbers: List['SN']) -> 'SN':
        base = numbers.pop(0)
        for n in numbers:
            if DEBUG > 1:
                print(" ", base)
                print("+", n)
            base = base + n
            if DEBUG > 1:
                print("=", base)
                print()
        return base

    @classmethod
    def arg_from_string(cls, string: str, pos: int):
        """Extract Regular number or another Snailfish number starting in
        given <string> at given position <pos>.
        Return extracted value and position just after the extract.
        """
        ch = string[pos]
        if ch.isdecimal():
            if string[pos+1].isdecimal():
                # Valid inputs do not contain numbers > 9 but some tests
                # inputs do.
                ch = string[pos:pos+2]
                if not cls.ALLOW_LONG_NUMBERS:
                    raise SNError(f"Unexpected long number at pos {pos}: {ch}")
            value = RN(ch)
            pos += len(value)
        elif ch == '[':
            value = cls.from_string(string, pos)
            pos = value.end
        else:
            raise SNError(f"Further parsing failed at {pos}: {ch}")
        return value, pos

    @classmethod
    def from_string(cls, string: str, pos: int = 0):
        # print("Looking at", string[pos:])
        this = cls()
        this.start = pos
        # opening bracket
        assert string[pos] == '[', \
               f"Wrong, must start with [ but got {string[pos]}"
        # extract 1st argument
        this.left, pos = cls.arg_from_string(string, 1+pos)
        # comma
        assert string[pos] == ',', \
            f"Expecting comma at {pos} but got {string[pos]}"
        # extract 2nd argument
        this.right, pos = cls.arg_from_string(string, 1+pos)
        # closing bracket
        assert string[pos] == ']', \
            f"Expecting ] at {pos} but got {string[pos]}"
        this.end = 1+pos  # skip ]
        return this

    def __init__(self, *args):
        self.args: List[Union['SN', 'RN']] = [None, None]
        if args:
            assert len(args) == 2, \
                f"Expecting 2 argument but got {len(args)}: {args}"
            self.left, self.right = args
        self.parent = None
        self.position = None
        # the following are required for parsing SN from string
        self.start: int = None
        self.end: int = None

    def __str__(self):
        return "[{},{}]".format(str(self.left), str(self.right))

    def __iter__(self):
        """DFS-like iterator"""
        for arg in (self.left, self.right):
            yield arg
            if isinstance(arg, type(self)):
                for item in arg:
                    yield item

    def __getitem__(self, pos):
        """Retrieve argument by position:
          0 -- left side arg, 1 -- right side argument
        """
        assert pos in {0,1}, f"Out of range: {pos}"
        return self.args[pos]

    def __setitem__(self, pos, other):
        assert pos in {0,1}, f"Out of range: {pos}"
        self.args[pos] = other
        other.parent = self
        other.position = pos

    def __add__(self, other: 'SN'):
        if self.left and other.left:
            new = SN(self, other)
            return new.reduce()
        elif self.left:
            return self
        else:
            return other

    @property
    def left(self):
        return self[0]

    @left.setter
    def left(self, other):
        self[0] = other

    @property
    def right(self):
        return self[1]

    @right.setter
    def right(self, other):
        self[1] = other

    @property
    def magnitude(self):
        return 3 * self.left.magnitude + 2 * self.right.magnitude

    @property
    def level(self):
        return 1 + (self.parent.level if self.parent else 0)

    def explode(self, left_neighbor, right_neighbor):
        if left_neighbor is not None:
            left_neighbor += self.left
        if right_neighbor is not None:
            right_neighbor += self.right
        self.parent[self.position] = RN(0)

    def reduce(self):
        changed = True
        while changed:
            changed = False

            if DEBUG > 1:
                print("--- reducing ---")
                print(self)
                numbers = self._get_numbers()
                print([n.value for n in numbers])

            changed = self._do_explode()
            if changed:
                continue

            changed = self._do_split()

        return self

    def _do_explode(self) -> bool:
        changed = False
        numbers = self._get_numbers()
        for i, num_i in enumerate(numbers):
            j = i+1
            if (num_i.parent.level > 4
                    and j < len(numbers) and num_i.is_sibling(numbers[j])):
                if DEBUG > 1:
                    print("Exploding", num_i.parent)
                prev = numbers[i-1] if i-1 >= 0 else None
                nxt = numbers[j+1] if j+1 < len(numbers) else None
                num_i.parent.explode(prev, nxt)
                if DEBUG > 1:
                    print("RESULT\t", self)
                changed = True
                break
        return changed

    def _do_split(self) -> bool:
        changed = False
        numbers = self._get_numbers()
        for num in numbers:
            if isinstance(num, RN) and num > 9:
                if DEBUG > 1:
                    print("Splitting", num)
                num.parent[num.position] = num.split()
                if DEBUG > 1:
                    print("RESULT\t", self)
                changed = True
                break
        return changed

    def _get_numbers(self) -> List['RN']:
        return [n for n in self if isinstance(n, RN)]


def test_explode_action():
    counts = [0, 0]
    tests = [
        ("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]"),
        ("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]"),
        ("[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]"),
        ("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]",
         "[[3,[2,[8,0]]],[9,[5,[7,0]]]]")
    ]
    for line, exp in tests:
        print("INPUT\t", line)
        sn = SN.from_string(line)
        sn.reduce()
        cmp = exp == str(sn)
        print("Equal? {}\n< {}\n> {}".format(cmp, exp, sn))
        counts[int(cmp)] += 1
    print("Failed/Ok: {}/{}".format(*counts))


def test_split_action():
    print("--- Splitting a Regular number ---")
    SN.ALLOW_LONG_NUMBERS = True
    tests = [("[10,11]", "[[5,5],[5,6]]")]
    counts = [0, 0]
    for line, exp in tests:
        print("INPUT\t", line)
        sn = SN.from_string(line)
        # sn.left = sn.left.split()  # low level method
        # sn.right = sn.right.split()  # low level method
        sn.reduce()
        print("RESULT\t", sn)
        cmp = exp == str(sn)
        print("Equal?", cmp)
        counts[int(cmp)] += 1
    print("Failed/Ok: {}/{}".format(*counts))
    SN.ALLOW_LONG_NUMBERS = False


def test_sn_traversal():
    print("--- Traversal from left to right ---")
    lines = tests[0][0]
    counts = [0, 0]
    for line in lines:
        line = lines[0]
        # all numbers as they appear in the string from left to right
        exp_values = list(map(int, filter(len, re.split(r'\D+', line))))
        # print(exp_values)
        sn = SN.from_string(line)
        print("NUMBER\t", sn)
        # traverse SN (in dfs order) and collect all numbers from it.
        values = []
        for arg in sn:
            # print(arg)
            if isinstance(arg, RN):
                values.append(int(arg))
        # Compare lists of numbers extracted using above two methods.
        # They must be equal.
        cmp = exp_values == values
        print("Extracted values equal? {}\n< {}\n> {}".format(
            cmp, exp_values, values))
        counts[int(cmp)] += 1
    print("Failed/Ok: {}/{}".format(*counts))


def test_sn_parsing():
    """Parse lines to Snailfish Numbers (SN), serialize them back to string
    and expect serialization to be equal to the source string."""
    print("--- Parsing a string into Snailfish Number ---")
    lines = tests[0][0]
    lines = utils.load_input()
    counts = [0, 0]
    for line in lines:
        sn = SN.from_string(line)
        print("INPUT\t", line)
        print("PARSED\t", sn)
        cmp = line == str(sn)
        print("Equal?", cmp)
        counts[int(cmp)] += 1
    print("Failed/Ok: {}/{}".format(*counts))


def test_sn_magnitude():
    line = "[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]"
    exp = 4140
    sn = SN.from_string(line)
    cmp = sn.magnitude == exp
    print("Magnitude correct?", exp, sn.magnitude, cmp)


def test_sn_level():
    counts = [0, 0]
    line = "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]"
    exp = [2,3,4,5,5,2,3,4,5,5] # level of nodes containing a number
    print("INPUT\t", line)
    sn = SN.from_string(line)
    levels = [n.parent.level for n in sn if isinstance(n, RN)]
    cmp = exp == levels
    print("Equal? {}\n< {}\n> {}".format(cmp, exp, levels))
    counts[int(cmp)] += 1
    print("Failed/Ok: {}/{}".format(*counts))


def test_sn_sum():
    counts = [0, 0]
    tests = [
        (["[[[[4,3],4],4],[7,[[8,4],9]]]", "[1,1]"],
          "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"),

        (["[1,1]", "[2,2]", "[3,3]", "[4,4]"],
          "[[[[1,1],[2,2]],[3,3]],[4,4]]"),

        (["[1,1]", "[2,2]", "[3,3]", "[4,4]", "[5,5]"],
          "[[[[3,0],[5,3]],[4,4]],[5,5]]"),

        (["[1,1]", "[2,2]", "[3,3]", "[4,4]", "[5,5]", "[6,6]"],
          "[[[[5,0],[7,4]],[5,5]],[6,6]]"),

        (utils.load_input('test.2.txt'),
         "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")
    ]
    for idx, (lines, exp) in enumerate(tests):
        print(f"--- Test {idx} ---")
        sns = [SN.from_string(ln) for ln in lines]
        res = SN.sum(sns)
        cmp = exp == str(res)
        print("Equal? {}\n< {}\n> {}".format(cmp, exp, res))
        counts[int(cmp)] += 1
    print("Failed/Ok: {}/{}".format(*counts))


# test_sn_parsing()
# test_sn_magnitude()
# test_sn_level()
# test_sn_traversal()
# test_split_action()
# test_explode_action()
# test_sn_sum()
# exit(100)


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    numbers = [SN.from_string(line) for line in lines]
    res = SN.sum(numbers)
    return res.magnitude


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    best = None
    arrangements = list(combinations(range(0, len(lines)), 2))
    arrangements.extend([list(reversed(arng)) for arng in arrangements])
    for idx, arrangement in enumerate(arrangements):
        sns = [SN.from_string(lines[i]) for i in arrangement]
        res = SN.sum(sns)
        if not best or best.magnitude < res.magnitude:
            best = res
        if DEBUG:
            print("[{}/{}] {}, {}; best is {} with {}".format(
                    idx, len(arrangements),
                    res.magnitude, res, arrangement,
                    best.magnitude))
    return best.magnitude


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
    exp1 = 3574
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = 4763
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()

