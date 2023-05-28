from typing import Optional
from ..entities.extractor import AbstractEntityExtractor
from ..entities.linkers import AbstractEntityLinker
from ..entities.context import ConText


class EntityPipeline:
    def __init__(self, \
                 entity_extractor: AbstractEntityExtractor, \
                 entity_linker: Optional[AbstractEntityLinker], \
                 context: Optional[ConText]):
        self._entity_extractor = entity_extractor
        self._entity_linker = entity_linker
        self._context = context

    def extract_data(self, text: str):
        entities = self._entity_extractor.get_entities(text)
        if self._entity_linker:
            entities = self._entity_linker.link(entities)

        if self._context:
            entities = self._context.apply(
                text,
                entities,
                filter_out_rule_labels=True
            )

        return entities
