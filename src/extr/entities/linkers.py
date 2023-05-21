from abc import ABC, abstractmethod
from typing import Dict, List
from ..models import Entity


class AbstractEntityLinker(ABC):
    def __init__(self, attribute_label: str) -> None:
        self._attribute_label = attribute_label

    @property
    def attribute_label(self) -> str:
        return self._attribute_label

    @abstractmethod
    def link(self, entities: List[Entity]) -> List[Entity]:
        pass

class KnowledgeBaseEntityLinker(AbstractEntityLinker):
    def __init__(self, attribute_label: str, kb: Dict[str, str]) -> None:
        super().__init__(attribute_label)
        self._kb = kb

    def link(self, entities: List[Entity]) -> List[Entity]:
        for entity in entities:
            key = entity.text

            if key in self._kb:
                entity.add_attribute(self._attribute_label, self._kb[key])

        return entities
