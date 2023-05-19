import os
import sys

sys.path.insert(0, os.path.join('../src'))

from extr.tokenizers import tokenizer, word_tokenizer


def test_tokenizer():
    token_groups = list(
        tokenizer(
            'Ted is a pitcher. We love going to see him.',
            [
                ['Ted', 'is', 'a', 'pitcher', '.'],
                ['We', 'love', 'going', 'to', 'see', 'him', '.']
            ]
        )
    )

    assert len(token_groups) == 2

    assert token_groups[0].location.start == 0
    assert token_groups[0].location.end == 17
    assert len(token_groups[0].tokens) == 5

    assert token_groups[1].location.start == 18
    assert token_groups[1].location.end == 43
    assert len(token_groups[1].tokens) == 7

def test_word_tokenizer():
    token_group = word_tokenizer(
        'Ted is a pitcher.',
        ['Ted', 'is', 'a', 'pitcher', '.']
    )

    assert token_group.location.start == 0
    assert token_group.location.end == 17
    assert len(token_group.tokens) == 5
