import os
import sys

sys.path.insert(0, os.path.join('../src'))

from extr.tokenizers import word_tokenizer


def test_word_tokenizer():
    token_group = word_tokenizer(
        'Ted is a pitcher.',
        ['Ted', 'is', 'a', 'pitcher', '.']
    )

    assert token_group.location.start == 0
    assert token_group.location.end == 17
    assert len(token_group.tokens) == 5
