from abc import ABC, abstractmethod
from typing import Callable, Generator, List, Optional, Set
from enum import Enum
from dataclasses import dataclass
from ..models import Entity, Token
from ..tokenizers import word_tokenizer as tokenizer


class DirectionType(Enum):
    LEFT=0
    RIGHT=1
    BOTH=2

class ConTextRule:
    def __init__(self,
                 attribute: str,
                 labels: List[str],
                 window_size: int = 5,
                 direction: DirectionType = DirectionType.RIGHT,
                 exit_labels: Optional[List[str]] = None) -> None:
        self._attribute = attribute
        self._labels = labels
        self._window_size = window_size
        self._direction = direction
        self._exit_labels = labels[:] + ([] if exit_labels is None else exit_labels)

    @property
    def attribute(self) -> str:
        return self._attribute

    @property
    def labels(self) -> List[str]:
        return self._labels

    @property
    def window_size(self) -> int:
        return self._window_size

    @property
    def direction(self) -> DirectionType:
        return self._direction

    @property
    def exit_labels(self) -> List[str]:
        return self._exit_labels

@dataclass
class ConTextRuleGroup:
    rules: List[ConTextRule]

    def get_rules(self, token: Token) -> Generator[ConTextRule, None, None]:
        entity_labels: Set[str] = set(entity.label for entity in token.entities)
        for rule in self.rules:
            if any(
                label
                for label in rule.labels
                if label in entity_labels
            ):
                yield rule

class AbstractConText(ABC):
    @abstractmethod
    def apply(self, text: str, entities: List[Entity], filter_out_rule_labels: bool = True) -> List[Entity]:
        pass

class ConText(AbstractConText):
    def __init__(self, \
                 rule_grouping: ConTextRuleGroup, \
                 word_tokenizer: Callable[[str], List[str]], \
                 attribute_label: str = 'ctypes') -> None:
        self._rule_grouping = rule_grouping
        self._word_tokenizer = word_tokenizer
        self._attribute_label = attribute_label

    @staticmethod
    def get_tokens_by_direction(current_index: int, window_size: int, direction: DirectionType, tokens: List[Token]) -> List[Token]:
        if direction == DirectionType.RIGHT:
            start = current_index + 1
            end = min([start + window_size, len(tokens)])
            return tokens[start:end]

        if direction == DirectionType.LEFT:
            start = max([current_index - 1 - window_size, 0])
            end = current_index
            return tokens[start:end][::-1]

        return []

    def apply(self, text: str, entities: List[Entity], filter_out_rule_labels: bool = True) -> List[Entity]:
        token_group = tokenizer(text, self._word_tokenizer(text))
        token_group.apply_entities(entities)

        tokens = token_group.tokens
        for current_index, token in enumerate(tokens):
            for rule in self._rule_grouping.get_rules(token):
                for tokens_by_direction in self._get_tokens_for_rule(
                    current_index,
                    rule,
                    tokens
                ):
                    self._process_direction_for_rule(rule, tokens_by_direction)

        if filter_out_rule_labels:
            all_labels: List[str] = []
            for rule in self._rule_grouping.rules:
                all_labels.extend(rule.labels)
                all_labels.extend(rule.exit_labels)

            labels = set(all_labels)

            return [
                entity
                for entity in entities
                if not entity.label in labels
            ]

        return entities

    def _get_tokens_for_rule(self, current_index: int, rule: ConTextRule, tokens: List[Token]) -> Generator[List[Token], None, None]:
        directions = [DirectionType.RIGHT, DirectionType.LEFT] \
            if rule.direction == DirectionType.BOTH \
            else [rule.direction]

        for direction in directions:
            yield ConText.get_tokens_by_direction(current_index, rule.window_size, direction, tokens)

    def _process_direction_for_rule(self, rule: ConTextRule, tokens: List[Token]) -> None:
        for token in tokens:
            exit_condition_met = any(
                entity
                for entity in token.entities
                if entity.label in rule.exit_labels
            )

            if exit_condition_met:
                break

            token.apply_attribute(self._attribute_label, rule.attribute)
