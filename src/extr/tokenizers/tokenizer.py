from typing import List, Generator, Union
from extr import Location
from ..models import Token, TokenGroup


def tokenizer(text: str, sentences: Union[Generator[List[str], None, None], List[List[str]]]) -> Generator[TokenGroup, None, None]:
    offset = 0
    cache = text[:]
    for sentence in sentences:
        counter = 0
        sentence_start = offset
        tokens_in_sentence = []
        for term in sentence:
            start = cache.find(term)
            end = start + len(term)

            actual_term = cache[start:end]
            assert actual_term == term, f'mismatch("{actual_term}", "{term}")'

            tokens_in_sentence.append(
                Token(term, Location(offset + start, offset + end), counter)
            )

            cache = cache[end:]
            offset += end
            counter += 1

        sentence_text = text[sentence_start:offset]

        yield TokenGroup(
            Location(sentence_start, offset),
            sentence_text,
            tokens_in_sentence
        )
