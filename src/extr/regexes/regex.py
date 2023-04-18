from typing import List, Tuple
import re

from ..iterutils import flatten


class RegEx:
    def __init__(self, expressions: List[str], flags: int = 0) -> None:
        self._expressions = expressions
        self._flags = flags

    def findall(self, text: str) -> List[re.Match]:
        def handler(expression: str) -> list:
            return list(re.finditer(expression, text, self._flags))

        return flatten(map(handler, self._expressions))

class RegExLabel:
    def __init__(self, label: str, regexes: List[RegEx]) -> None:
        self._label = label
        self._regexes = regexes

    def findall(self, text: str) -> List[Tuple[str, re.Match]]:
        def handler(regex) -> list:
            observations = regex.findall(text)
            return list(zip([self._label] * len(observations), observations))

        return flatten(map(handler, self._regexes))
