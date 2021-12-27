import os
import sys
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

from .solution import Monad, model_numbers


@pytest.fixture
def validator_1():
    return Monad.from_lines(utils.load_input('test.1.txt'))

@pytest.fixture
def validator_2():
    return Monad.from_lines(utils.load_input('test.2.txt'))

@pytest.fixture
def monad():
    return Monad.from_lines(utils.load_input('input.txt'))


def test_1(validator_1):
    assert len(validator_1.instructions) == 4, "Instruction set length wrong"


@pytest.mark.parametrize("inputs, exp", [
    ([3, 9], 1),
    ([1, 3], 1),
    ([0, 0], 1),
    ([-1, -3], 1),
    ([3, 10], 0),
    ([2, 5], 0),
    # ("39", 1),
    # ("25", 0)
])
def test_2(validator_1, inputs, exp):
    validator_1.exec(inputs)
    assert validator_1.registers['z'] == exp, \
        "Failed for inputs={} exp={}".format(inputs, exp)


@pytest.mark.parametrize("inputs, exp", [
    ([0], [0,0,0,0]),
    ([1], [0,0,0,1]),
    ([2], [0,0,1,0]),
    ([15], [1,1,1,1])
])
def test_3(validator_2, inputs, exp):
    validator_2.exec(inputs)
    res = [validator_2.registers[k] for k in ['w', 'x', 'y', 'z']]
    assert exp == res, \
             "Failed for inputs={} exp={} but got {}".format(inputs, exp, res)


#def test_4(monad):
#    modelno = list(map(int, list("13579246899999")))
#    res = monad.is_valid(modelno)
#    print(res)
#    print(monad.registers)
#    assert False
