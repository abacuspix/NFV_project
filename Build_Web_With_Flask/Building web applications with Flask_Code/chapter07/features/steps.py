# coding:utf-8

from lettuce import *
from ex01 import sum_fnc


@step('Given I have the numbers (\-?\d+) and (\-?\d+)')
def have_the_numbers(step, *numbers):
    numbers = map(lambda n: int(n), numbers)
    world.numbers = numbers

@step('When I sum them')
def compute_sum(step):
    world.result = sum_fnc(*world.numbers)

@step('Then I see the result (\-?\d+)')
def check_number(step, expected):
    expected = int(expected)
    assert world.result == expected, "Got %d; expected %d" % (world.result, expected)