from typing import List
from extr import Location
from ..models import Token, TokenGroup


def word_tokenizer(text: str, tokens: List[str]) -> TokenGroup:
    cache = text[:]

    offset = 0
    tokens_in_sentence: List[Token] = []
    for term in tokens:
        start = cache.find(term)
        end = start + len(term)

        actual_term = cache[start:end]
        assert actual_term == term, f'mismatch("{actual_term}", "{term}")'

        tokens_in_sentence.append(
            Token(term, Location(offset + start, offset + end), len(tokens_in_sentence) + 1)
        )

        cache = cache[end:]
        offset += end

    sentence_start = tokens_in_sentence[0].location.start
    sentence_end = tokens_in_sentence[-1].location.end

    token_group = TokenGroup(
        Location(sentence_start, sentence_end),
        text[sentence_start:sentence_end],
        tokens_in_sentence
    )

    return token_group
