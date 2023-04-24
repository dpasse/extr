import os
import sys
import re

sys.path.insert(0, os.path.join('../src'))

from extr.regexes import RegEx, SlimRegEx


def test_findall():
    regex = RegEx(
        expressions=[
            r'.+',
        ]
    )

    text = 'Ted is a pitcher.'

    matches = regex.findall(text)
    assert len(matches) == 1
    assert matches[0].group() == text


def test_findall_with_skip_ifs():
    regex = RegEx(
        expressions=[
            r'.+',
        ],
        skip_if=[
            SlimRegEx([r'is\s+a'])
        ],
    )

    matches = regex.findall('Ted is a pitcher.')
    assert len(matches) == 0
