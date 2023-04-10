from typing import List, Tuple

import re
from .iterutils import flatten


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

class RegExRelationLabel:
    def __init__(self, label: str) -> None:
        self._label = label
        self._expressions: List[RegEx] = []

    @property
    def label(self) -> str:
        return self._label

    def create_regex_label(self) -> RegExLabel:
        return RegExLabel(
            self.label,
            self._expressions
        )

    def add_e1_to_e2(self, e1: str, relation_expressions: List[str], e2: str) -> None:
        self._expressions.append(
            RegEx(
                list(
                    map(
                        lambda expression: r'(?P<e1>##ENTITY_' + e1 + r'_\d+##)' + expression + r'(?P<e2>##ENTITY_' + e2 + r'_\d+##)',
                        relation_expressions
                    )
                )
            )
        )

    def add_e2_to_e1(self, e2: str, relation_expressions: List[str], e1: str) -> None:
        self._expressions.append(
            RegEx(
                list(
                    map(
                        lambda expression: r'(?P<e2>##ENTITY_' + e2 + r'_\d+##)' + expression + r'(?P<e1>##ENTITY_' + e1 + r'_\d+##)',
                        relation_expressions
                    )
                )
            )
        )