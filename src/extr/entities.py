from typing import List, cast

from .regex import RegExLabel
from .iterutils import flatten
from .models import Location, Entity, EntityAnnotationResults


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

class EntityAnnotator:
    def annotate(self, text: str, entities: List[Entity]) -> EntityAnnotationResults:
        def insert_entity(text: str, entity: Entity) -> str:
            return text[:entity.start] + str(entity) + text[entity.end:]

        annotated_text = text[:]
        for identifer, entity in enumerate(entities):
            entity.identifier = identifer + 1
            annotated_text = insert_entity(annotated_text, entity)

        return EntityAnnotationResults(text, annotated_text, entities)
