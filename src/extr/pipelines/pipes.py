from typing import Optional, List, Tuple
from ..models import Entity, Relation
from ..entities.extractor import AbstractEntityExtractor
from ..entities.annotator import EntityAnnotator
from ..entities.linkers import AbstractEntityLinker
from ..entities.context import ConText
from ..relations.extractor import RelationExtractor


class EntityPipeline:
    def __init__(self, \
                 entity_extractor: AbstractEntityExtractor, \
                 entity_linker: Optional[AbstractEntityLinker], \
                 context: Optional[ConText]):
        self._entity_extractor = entity_extractor
        self._entity_linker = entity_linker
        self._context = context

    def extract(self, text: str) -> List[Entity]:
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

class RelationPipeline:
    def __init__(self, \
                 entity_pipeline: EntityPipeline,
                 entity_annotator: EntityAnnotator,
                 relation_extractor: RelationExtractor):
        self._entity_pipeline = entity_pipeline
        self._entity_annotator = entity_annotator
        self._relation_extractor = relation_extractor

    def extract(self, text: str) -> Tuple[List[Entity], List[Relation]]:
        entities = self._entity_pipeline.extract(text)
        relations = self._relation_extractor.extract(
            self._entity_annotator.annotate(text, entities),
            entities
        )

        return entities, relations
