from typing import List, cast

from .regex import RegExLabel
from .iterutils import flatten
from .models import Entity, EntityAnnotationResults, Location


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
        all_found_labels = sorted(
            cast(List[Entity], flatten(map(handler, self._regex_labels))),
            key=lambda entity: (entity.end, -entity.start),
            reverse=True
        )

        if len(all_found_labels) == 0:
            return []

        labels = all_found_labels[:1]
        for curr_label in all_found_labels[1:]:
            prev_label = labels[-1]

            if curr_label.location.is_in(prev_label.location):
                continue

            labels.append(curr_label)

        return labels

class EntityAnnotator:
    def annotate(self, text: str, entities: List[Entity]) -> EntityAnnotationResults:
        annotated_text = text[:]
        for identifer, entity in enumerate(entities):
            entity.identifer = identifer + 1
            annotated_text = annotated_text[:entity.start] + str(entity) + annotated_text[entity.end:]

        return EntityAnnotationResults(text, annotated_text, entities)
