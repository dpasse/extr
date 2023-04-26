from typing import List, cast

from ..regexes import RegExLabel
from ..utils import flatten
from ..models import Location, Entity


class EntityExtractor:
    def __init__(self, regex_labels: List[RegExLabel]) -> None:
        self._regex_labels = regex_labels

    def get_entities(self, text: str) -> List[Entity]:
        def handler(regex_label: RegExLabel):
            return (
                Entity(label, match.group(), Location(*match.span()))
                for label, match in regex_label.findall(text)
            )

        ## sort descending
        all_found_entities = sorted(
            cast(List[Entity], flatten(map(handler, self._regex_labels))),
            key=lambda entity: (entity.end, -entity.start),
            reverse=True
        )

        if len(all_found_entities) == 0:
            return []

        entities = all_found_entities[:1]
        for curr_entity in all_found_entities[1:]:
            prev_entity = entities[-1]

            if curr_entity.is_in(prev_entity):
                continue

            entities.append(curr_entity)

        return entities
