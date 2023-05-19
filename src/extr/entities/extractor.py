from abc import ABC, abstractmethod
from typing import List

from ..regexes import RegExLabel
from ..models import Location, Entity


class AbstractEntityExtractor(ABC):
    @abstractmethod
    def get_entities(self, text: str) -> List[Entity]:
        pass

class EntityExtractor(AbstractEntityExtractor):
    def __init__(self, regex_labels: List[RegExLabel]) -> None:
        self._regex_labels = regex_labels

    def get_entities(self, text: str) -> List[Entity]:
        entities: List[Entity] = []
        for regex_label in self._regex_labels:
            for label, match in regex_label.findall(text):
                entities.append(
                    Entity(
                        len(entities) + 1,
                        label,
                        match.group(),
                        Location(*match.span())
                    )
                )

        if len(entities) == 0:
            return []

        ## sort descending
        all_found_entities = sorted(
            entities,
            key=lambda entity: (entity.end, -entity.start),
            reverse=True
        )

        entities = all_found_entities[:1]
        for curr_entity in all_found_entities[1:]:
            prev_entity = entities[-1]

            if curr_entity.is_in(prev_entity):
                continue

            entities.append(curr_entity)

        return entities
