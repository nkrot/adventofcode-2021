#!/usr/bin/env python

# # #
#
#

import os
import sys
import json
from typing import List
from functools import reduce

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '16'
DEBUG = False


HEX2BIN = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


def hex2bin(msg: str):
    return "".join([HEX2BIN[ch] for ch in msg])


def bin2dec(words: List[str]):
    if isinstance(words, str):
        word = words
    else:
        word = "".join(words)
    return int(word, 2)


def get_version(buffer, start):
    word = buffer[start:start+3]
    res = (bin2dec(word), start+3)
    if DEBUG:
        print("VERSION\t", res, word)
    return res


def get_packet_type_id(buffer, start):
    word = buffer[start:start+3]
    res = (bin2dec(word), start+3)
    if DEBUG:
        print("TYPE_ID\t", res, word)
    return res


def get_literal(buffer, start = 0, end = None):
    # TODO: what is the correct value of end offset?
    end = end or len(buffer)
    words = []
    while start < end:
        words.append(buffer[start+1:start+5])
        if buffer[start] == "0":
            start += 5
            break
        start += 5
    val = bin2dec(words)
    res = (val, start)
    if DEBUG:
        print("LITERAL\t", res, words)
        print("TAIL\t", buffer[start:end])
    return res


def get_length_type_id(buffer, start):
    word = buffer[start:start+1]
    res = (bin2dec(word), start+1)
    if DEBUG:
        print("LENGTH_TYPE_ID", res, word)
    return res


def get_length(buffer, start, length):
    end = start + length
    word = buffer[start:end]
    res = (bin2dec(word), end)
    if DEBUG:
        print("LENGTH", res, word)
    return res


def parse_operator_packet(buffer, start, end):
    packets = []
    len_type_id, start = get_length_type_id(buffer, start)
    if len_type_id == 0:
        # retrieve unspecified number of subpackets that fit within given length
        length, start = get_length(buffer, start, 15)
        end = start + length
        while end - start > 5:
            p, start = parse_packet(buffer, start, end)
            packets.append(p)
    elif len_type_id == 1:
        # retrieve specific number of subpackets
        count, start = get_length(buffer, start, 11)
        for _ in range(count):
            p, start = parse_packet(buffer, start, end)
            packets.append(p)
    else:
        raise ValueError(f"Unrecognized LENGTH_TYPE_ID: {len_type_id}")
    return packets, start


def parse_packet(buffer, start, end):
    packet = {}
    packet['version'], start = get_version(buffer, start)
    packet['typeid'], start = get_packet_type_id(buffer, start)
    if packet['typeid'] == 4:
        packet["value"], start = get_literal(buffer, start, end)
    else:
        packet["operator"], start = parse_operator_packet(buffer, start, end)
    return (packet, start)


def collect_versions(pkt, collected):
    for k in pkt:
        if k == 'version':
            collected.append(pkt[k])
        if k == 'operator':
            for subpkt in pkt[k]:
                collect_versions(subpkt, collected)


def evaluate(packet: dict):
    """recursively"""
    typeid = packet['typeid']

    if typeid == 4:
        return packet['value']

    values = [evaluate(subpkt) for subpkt in packet['operator']]

    if typeid == 0:
        return sum(values)
    elif typeid == 1:
        return reduce(lambda a, b: a*b, values, 1)
    elif typeid == 2:
        return min(values)
    elif typeid == 3:
        return max(values)
    elif typeid == 5:
        assert len(values) == 2, \
                "Wrong number of arguments, msut be 2 but got {}".format(len(values))
        return int(values[0] > values[1])
    elif typeid == 6:
        assert len(values) == 2, \
                "Wrong number of arguments, msut be 2 but got {}".format(len(values))
        return int(values[0] < values[1])
    elif typeid == 7:
        assert len(values) == 2, \
                "Wrong number of arguments, msut be 2 but got {}".format(len(values))
        return int(values[0] == values[1])

    raise ValueError(f"Unknown operator with typeid={typeid}")


def solve_p1(line: str) -> int:
    """Solution to the 1st part of the challenge"""
    buffer = hex2bin(line)
    if DEBUG:
        print("BUFFER", buffer)

    packet, _ = parse_packet(buffer, 0, len(buffer))

    if DEBUG:
        print("-- packet --")
        print(json.dumps(packet, indent=2))
                
    versions = []
    collect_versions(packet, versions)
    return sum(versions)


def solve_p2(line: str) -> int:
    """Solution to the 2nd part of the challenge"""
    buffer = hex2bin(line)
    packet, _ = parse_packet(buffer, 0, len(buffer))
    return evaluate(packet)


text_1 = "D2FE28"
text_2 = "38006F45291200"
text_3 = "EE00D40C823060"

assert hex2bin(text_1) == "110100101111111000101000"
assert hex2bin(text_2) == "00111000000000000110111101000101001010010001001000000000"
assert hex2bin(text_3) == "11101110000000001101010000001100100000100011000001100000"

assert bin2dec(["0111", "1110", "0101"]) == 2021, "bin2dec failed"
assert bin2dec("000000000011011") == 27, "bin2dec failed"


tests = [
    (text_1, 6, 2021),
    (text_2, 9, 1),
    (text_3, 14, 3),
    ("8A004A801A8002F478", 4+1+5+6, 15),
    ("620080001611562C8802118E34", 12, 46),
    ("C0015000016115A2E0802F182340", 23, 46),
    ("A0016C880162017C3686B18A3D4780", 31, 54),
    ("C200B40A82", 14, 3),
    ("04005AC33890", 8, 6*9),
    ("880086C3E88112", 15, 7),
    ("CE00C43D881120", 11, 9),
    ("D8005AC2A8F0", 13, 1),
    ("F600BC2D8F", 19, 0),
    ("9C005AC2F8F0", 16, 0),
    ("9C0141080250320F1802104A08", 20, 1)
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
    lines = utils.load_input()[0]

    print(f"--- Day {DAY} p.1 ---")
    exp1 = 920
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = 10185143721112
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
