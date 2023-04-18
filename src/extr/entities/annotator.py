from typing import List

from ..models import Entity, EntityAnnotationResults


class EntityAnnotator:
    def annotate(self, text: str, entities: List[Entity]) -> EntityAnnotationResults:
        def insert_entity(text: str, entity: Entity) -> str:
            return text[:entity.start] + str(entity) + text[entity.end:]

        annotated_text = text[:]
        for identifer, entity in enumerate(entities):
            entity.identifier = identifer + 1
            annotated_text = insert_entity(annotated_text, entity)

        return EntityAnnotationResults(text, annotated_text, entities)
