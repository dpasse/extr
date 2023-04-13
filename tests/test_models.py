import os
import sys
import re

sys.path.insert(0, os.path.join('../src'))

from extr import Location


def test_location_bigger_location_contains_smaller():
    big = Location(0, 10)
    small = Location(3, 7)

    assert big.contains(small)

def test_location_contains_returns_false_on_partial_fit_1():
    big = Location(0, 10)
    small = Location(7, 12)

    assert not big.contains(small)

def test_location_contains_returns_false_on_partial_fit_2():
    big = Location(5, 10)
    small = Location(3, 8)

    assert not big.contains(small)

def test_location_contains_return_false_when_given_larger():
    big = Location(5, 10)
    small = Location(3, 12)

    assert not big.contains(small)

def test_location_is_in_returns_true_when_completely_in_other():
    location1 = Location(3, 12)
    location2 = Location(5, 10)

    assert location2.is_in(location1)

def test_location_is_in_returns_true_when_start_is_in_other():
    location1 = Location(3, 12)
    location2 = Location(5, 15)

    assert location2.is_in(location1)

def test_location_is_in_returns_true_when_end_is_in_other():
    location1 = Location(3, 12)
    location2 = Location(1, 5)

    assert location2.is_in(location1)

def test_location_is_in_returns_false_when_neither_is_in_other():
    location1 = Location(3, 12)
    location2 = Location(1, 3)

    assert not location2.is_in(location1)
