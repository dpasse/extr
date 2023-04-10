from typing import List, Generator

import re
from .regex import RegExLabel
from .entities import EntityAnnotationResults
from .iterutils import flatten
from .models import Relation


class RelationExtractor:
    def __init__(self, relation_labels: List[RegExLabel]) -> None:
        self._relation_labels = relation_labels

    def extract(self, entity_annotation_results: EntityAnnotationResults) -> List[Relation]:
        entity_lookup = entity_annotation_results.entity_lookup

        def create_relation(label, match: re.Match) -> Relation:
            group = match.groupdict()
            e1_key = group['e1']
            e2_key = group['e2']

            return Relation(
                label,
                entity_lookup[e1_key],
                entity_lookup[e2_key]
            )

        def handler(relationship_label: RegExLabel) -> Generator[Relation, None, None]:
            return (
                create_relation(label, match)
                for label, match in relationship_label.findall(entity_annotation_results.annotated_text)
            )

        return flatten(map(handler, self._relation_labels))
