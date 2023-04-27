from typing import List, Tuple, Optional
import re

from ..utils.iterutils import flatten


class SlimRegEx:
    def __init__(self, expressions: List[str], flags: int = 0) -> None:
        self._expressions = expressions
        self._flags = flags

    def findall(self, text: str) -> List[re.Match]:
        def handler(expression: str) -> list:
            return list(re.finditer(expression, text, self._flags))

        return flatten(map(handler, self._expressions))

    def search(self, text: str) -> Optional[re.Match]:
        for expression in self._expressions:
            match = re.search(expression, text)
            if match:
                return match

        return None

class RegEx(SlimRegEx):
    def __init__(self, expressions: List[str], flags: int = 0, skip_if: Optional[List[SlimRegEx]] = None) -> None:
        super().__init__(expressions, flags)

        self._skip_if = set([] if skip_if is None else skip_if)

    def findall(self, text: str) -> List[re.Match]:
        def handler(expression: str) -> list:
            observations = []
            for match in re.finditer(expression, text, self._flags):

                should_skip_match = False
                for skip_if in self._skip_if:
                    if skip_if.search(match.group()):
                        should_skip_match = True
                        break

                if not should_skip_match:
                    observations.append(match)

            return observations

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

def transform_knowledge(label: str, knowledge: List[str]) -> RegExLabel:
    expressions = [
        r'(?<!\w)' + term + r'(?!\w)'
        for term in knowledge
    ]

    return RegExLabel(
        label,
        [
            RegEx(expressions)
        ]
    )
