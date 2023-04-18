from typing import List

from ..models import Entity, EntityAnnotationResults


class EntityAnnotator:
    def annotate(self, text: str, entities: List[Entity], offset = 0) -> EntityAnnotationResults:
        def insert_entity(text: str, entity: Entity) -> str:
            start = entity.start - offset
            end = entity.end - offset
            return text[:start] + str(entity) + text[end:]

        annotated_text = text[:]
        for identifer, entity in enumerate(entities):
            entity.identifier = identifer + 1
            annotated_text = insert_entity(annotated_text, entity)

        return EntityAnnotationResults(text, annotated_text, entities)
