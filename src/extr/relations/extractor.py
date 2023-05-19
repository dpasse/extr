from abc import ABC, abstractmethod
from typing import List, Generator, cast

import re
from ..regexes import RegExLabel
from ..models import Relation, Entity
from ..utils import flatten


class AbstractRelationExtractor(ABC):
    @abstractmethod
    def extract(self, text: str, entities: List[Entity]) -> List[Relation]:
        pass

class RelationExtractor(AbstractRelationExtractor):
    def __init__(self, relation_labels: List[RegExLabel]) -> None:
        self._relation_labels = relation_labels

    def extract(self, text: str, entities: List[Entity]) -> List[Relation]:
        entity_lookup = { str(entity): entity for entity in entities }

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
                for label, match in relationship_label.findall(text)
            )

        return cast(List[Relation], flatten(map(handler, self._relation_labels)))
