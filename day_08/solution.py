#!/usr/bin/env python

# # #
# TODO: refactor decode_rec_old to make the solution readable
#
# time -p (decode)
# real 0,33
# user 0,30
# sys 0,01
#
# time -p (decode2 + decode_rec_old)
# real 45,43
# user 45,00
# sys 0,09


import os
import sys
from typing import List, Tuple
from collections import defaultdict
from itertools import permutations


sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DAY = '08'
DEBUG = True


CODES = {
    "0": "abcefg",  # 6
    "1": "cf",      # 2 !
    "2": "acdeg",   # 5
    "3": "acdfg",   # 5
    "4": "bcdf",    # 4 !
    "5": "abdfg",   # 5
    "6": "abdefg",  # 6
    "7": "acf",     # 3 !
    "8": "abcdefg", # 7 !
    "9": "abcdfg",  # 6
}

DECODES = {v: k for k,v in CODES.items()}

assert len(CODES) == len(DECODES), "Shit happened"


class Cipher(dict):

    @classmethod
    def sortchars(cls, signal: str):
        return "".join(sorted(list(signal)))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def extract_unknown(self, src: str, trg: str) -> Tuple[List[str], List[str]]:
        _src = [ch for ch in src if ch not in self.keys()]
        _trg = [ch for ch in trg if ch not in self.values()]
        return _src, _trg

    def to_seg(self, signal: str):
        """Convert signal to signal with segments rearranged.
        Use ? for unknown segments.
        """
        return "".join(self.get(ch, '?') for ch in signal)

    def decode(self, signal: str):
        dec = self.sortchars(self.to_seg(signal))
        return DECODES.get(dec, None)

    def update(self, other) -> bool:
        """Return if update was successful"""
        added = 0
        for src, trg in other:
            if src in self:
                # do not allow overriding
                return False
            else:
                self[src] = trg
                added += 1
        return added > 0


def printv(items):
    for item in items:
        print(item)


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    total = 0
    for line in lines:
        # print(line)
        notes = line.replace('|', '').split()
        output_values = notes[-4:]
        # print(output_values)
        total += sum(1 for v in output_values if len(v) in {2,4,3,7})
    return total


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    s = 0
    for line in lines:
        # print("INPUT", line)
        displays = line.replace('|', '').split()
        s += decode(displays)
    # print("TASK RESULT", s)
    return s


def read_displays(cipher, displays):
    n = len(displays)
    res = 0
    for idx, disp in enumerate(reversed(displays)):
        dec = cipher.decode(disp)
        inc = int(dec) * (10 ** idx)
        res += inc
    return res


def candidates_by_length():
    lengths = defaultdict(list)
    for digit, segments in CODES.items():
        lengths[len(segments)].append(digit)
    return lengths


def decode(displays):
    """
    Details
    1) a Cipher is a mapping of segments
    2) generate all possible ciphers and select those that can *fully* decode
       *all* displays to something meaningful.
    3) if necessary, check that selected cipher(s) decode(s) the displays to
       expected digit(s).
    4) Expected digits are computed based on the number of active segments
       on a display and the number of segments that must be active to indicate
       each of the digits. This is in <candidates>
    """

    # print(displays)

    # We will need it to suggest candidate digits for each 7-segment display:
    # the number of active segments corresponds to one or more possible digits.
    candidates = candidates_by_length()

    segments = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    readings = []

    # (2) generate all possible ciphers
    for perm in permutations(segments, len(segments)):
        cipher = Cipher(zip(segments, perm))
        decoded = [cipher.decode(d) for d in displays]

        # (2) the cipher that fails to decode *all* items is not suitable
        if None in decoded:
            continue

        # print(cipher)
        # print(decoded)
        # print("OK")

        # (3) Additionally check that the cipher decodes displays correctly:
        # For each display, we know a short list of numbers it can represent.
        # Here we check if decoded number is among those candidate numbers.
        checks = [dec in candidates[len(disp)]
                  for disp, dec in zip(displays, decoded)]

        if all(checks):
            reading = read_displays(cipher, displays[-4:])
            readings.append(reading)

    assert len(readings) == 1, "Expecting a single output from the displays"

    return readings[0]


def decode2(displays):
    # TODO: unfinished refactoring of decode_rec
    print(displays)

    lengths = candidates_by_length()

    displays = [Cipher.sortchars(d) for d in displays]

    _displays = [(disp, lengths[len(disp)]) for disp in set(displays)]

    _displays = sorted(_displays, key=lambda d: (len(d[0]), d[0]))

    # printv(_displays)

    ciphers = []
    decode_rec(_displays, Cipher(), ciphers)

    return 0
    # print(displays)
    # print("CIPHER", type(cipher), cipher)

    n = 4
    res = 0
    for idx, disp in enumerate(reversed(displays[-n:])):
        dec = cipher.decode(disp)
        # print(disp, dec, type(dec))
        inc = int(dec) * (10 ** idx)
        res += inc

    # print("LINE RESULT", res)
    return res


DEPTH = 0

def decode_rec(displays: list, cipher: dict):
    """An attempt to refactor decode_rec_old"""
    global DEPTH
    DEPTH += 1

    if DEBUG:
        print(f"--- LEVEL {DEPTH} ---")
        print("Number of displays: {};".format(len(displays)))
        printv(displays)
        print("Cipher state {}: {}".format(len(cipher), cipher))

    if not displays:
        print("DONE", cipher)
        return [cipher]

    current = displays.pop(0)
    display_info(current, cipher, "Checking ")

    signal, digits = current

    if len(digits) == 1:
        digit = digits[0]
        for _cipher in extend_cipher(cipher, signal, CODES[digit]):
            print(_cipher)

    return [cipher] # fake


def decode_rec_old(displays: list, cipher: dict, *args):
    """works but is ugly and needs to be refactored"""
    global DEPTH
    DEPTH += 1

    if DEBUG:
        print(f"--- LEVEL {DEPTH} ---")
        print("Number of displays: {};".format(len(displays)))
        printv(displays)
        print("Cipher state {}: {}".format(len(cipher), cipher))

    # remove cases that can be fully decoded
    # TODO: the order of <displays> is important
    displays, removed, removed_ids = remove_decodable(displays, cipher)

    if len(cipher) == 7 and not displays:
        # print("DONE", cipher)
        return [cipher]

    assert(displays), "Unexpected shit happened"

    if cipher:
        if not removed_ids:
            # print("..impossible. could not remove candidates")
            return []
        if 0 not in removed_ids:
            # print("..impossible. could not remove the 1st display")
            return []

    # TODO: make it into a queue: retrieve item, analyse it (and remaining items)
    # and if necessary, put it back into the queue. this will make the logic
    # simpler, as the outer loop will not be necessary: we always consider
    # the 1st items only.

    for idx in range(len(displays)):
        # print("Checking", displays[idx])
        # display_info(displays[idx], cipher, "Checking ")

        signal, digits = displays[idx]

        # TODO: these two branches have identical logic. DRY it

        if len(digits) == 1:
            # print("Simple case")
            for _cipher in extend_cipher(cipher, signal, CODES[digits[0]]):
                _displays = [displays[idx]] + displays[:idx] + displays[1+idx:]
                for new_cipher in filter(bool, decode_rec(_displays, _cipher)):
                    DEPTH -= 1
                    return [new_cipher]

        else:
            # print("Multiple case")
            for digit in digits:
                disp = (signal, [digit])
                # print("Trying", disp)
                _displays = [disp]

                for _disp in displays[:idx] + displays[1+idx:]:
                    if digit in _disp[1]:
                        _digits = list(_disp[1])
                        _digits.remove(digit)
                        _disp = (_disp[0], _digits)
                    _displays.append(_disp)

                for _cipher in extend_cipher(cipher, signal, CODES[digit]):
                    # display_info(disp, _cipher, "..")
                    # TODO: decode display with _cipher and check if deciphered number
                    # is in digits. If not, there is no need to recurse.
                    for new_cipher in filter(bool, decode_rec(_displays, _cipher)):
                        DEPTH -= 1
                        return [new_cipher]

            # print("..impossible")
            # return []

    DEPTH -= 1
    return []


def display_info(display, cipher, prefix=''):
    signal = display[0]
    print("{}Display {} --> {} --> {}".format(
        prefix, display, cipher.to_seg(signal), cipher.decode(signal)))


def remove_decodable(displays, cipher):
    selected = []
    removed = []
    seen_values = []
    removed_ids = []
    for idx, disp in enumerate(displays):
        decoded_value = cipher.decode(disp[0])
        # TODO: this is kinds shit that only the 1st occurrence is removed
        # this means that the items must be in the correct order
        if [decoded_value] == disp[1] and decoded_value not in seen_values:
            # print("Fully decodable:", disp, decoded_value)
            removed.append(disp)
            seen_values.append(decoded_value)
            removed_ids.append(idx)
        else:
            selected.append(disp)
    return selected, removed, removed_ids


def extend_cipher(cipher: dict, code1: str, code2: str):

    if DEBUG:
        print(".. extending from {} and {}".format(code1, code2))

    chars1, chars2 = cipher.extract_unknown(code1, code2)
    # print("New Pairs from", chars1, chars2)

    # TODO: this is logically correct but the solved does not converge
    # there can be a bug outside. W/o this rejectin condition, the original
    # cipher is also returned.
    # if not chars1:
    if len(chars1) != len(chars2):
        # or raise StopIteration
        return

    # print("..using")

    for chs in permutations(chars1, len(chars1)):
        # print(chs, len(chars1))
        # new_pairs = Cipher(zip(chs, chars2))
        # print(new_pairs)
        new_cipher = Cipher(cipher)

        # TODO:
        # if new_cipher.update(zip(chs, chars2))
        #     yield new_cipher

        # TODO: there is a bug here, ok is true (and new_cipher is returned)
        # even if new_cipher is equal to cipher (update was zero)
        ok = True
        for f, t in zip(chs, chars2):
            if f not in new_cipher:
                new_cipher[f] = t
            else:
                ok = False
        if ok:
            # print("yield", new_cipher)
            yield new_cipher


text_2 = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"
text_3 = "dbafgec ce cgefdb abged aedc bec deafgb cbage edgbac gfacb | abcfg edca febdcg ecb"

tests = [
         (utils.load_input('test.1.txt'), 26, None),
         ([text_2], None, 5353),
         ([text_3], None, 2407)
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
    exp1 = 294
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = 973292
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    # run_real()
