import os
import sys

sys.path.insert(0, os.path.join('../src'))

from extr.tokenizers import tokenizer


def test_get_entities():
    token_groups = list(
        tokenizer(
            'Ted is a pitcher.',
            [['Ted', 'is', 'a', 'pitcher', '.']]
        )
    )

    assert len(token_groups) == 1
    assert token_groups[0].location.start == 0
    assert token_groups[0].location.end == 17
    assert len(token_groups[0].tokens) == 5
