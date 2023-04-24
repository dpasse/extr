from typing import List, TypeVar
from dataclasses import dataclass, field

from ..regexes import RegEx, RegExLabel


# pylint: disable=C0103
TRegExRelationLabelBuilder = TypeVar('TRegExRelationLabelBuilder', bound='RegExRelationLabelBuilder')
# pylint: enable=C0103

@dataclass
class RelationLabelBuilderConfig:
    flags: int = 0
    skip_if: List[str] = field(default_factory=lambda: [])

class RegExRelationLabelBuilder:
    def __init__(self: TRegExRelationLabelBuilder, label: str) -> None:
        self._label = label
        self._expressions: List[RegEx] = []

    @property
    def label(self: TRegExRelationLabelBuilder) -> str:
        return self._label

    def add_e1_to_e2(self: TRegExRelationLabelBuilder, \
                     e1: str, relation_expressions: List[str], \
                     e2: str, config = RelationLabelBuilderConfig() \
    ) -> TRegExRelationLabelBuilder:
        self._expressions.append(
            RegEx(
                expressions=list(
                    map(
                        lambda expression: r'(?P<e1>##ENTITY_' + e1 + r'_\d+##)' + expression + r'(?P<e2>##ENTITY_' + e2 + r'_\d+##)',
                        relation_expressions
                    )
                ),
                flags=config.flags,
                skip_if=config.skip_if
            )
        )

        return self

    def add_e2_to_e1(self: TRegExRelationLabelBuilder, e2: str, \
                     relation_expressions: List[str], \
                     e1: str, config = RelationLabelBuilderConfig() \
    ) -> TRegExRelationLabelBuilder:
        self._expressions.append(
            RegEx(
                expressions=list(
                    map(
                        lambda expression: r'(?P<e2>##ENTITY_' + e2 + r'_\d+##)' + expression + r'(?P<e1>##ENTITY_' + e1 + r'_\d+##)',
                        relation_expressions
                    )
                ),
                flags=config.flags,
                skip_if=config.skip_if
            )
        )

        return self

    def build(self: TRegExRelationLabelBuilder) -> RegExLabel:
        return RegExLabel(self.label, self._expressions)
