from typing import List, Optional, Set
import re

from ..models import Entity, EntityAnnotationResults


class EntityAnnotator:
    def display_entity(self, entity: Entity) -> str:
        return str(entity)

    def annotate(self, text: str, entities: List[Entity], offset = 0) -> EntityAnnotationResults:
        def insert_entity(text: str, entity: Entity) -> str:
            start = entity.start - offset
            end = entity.end - offset
            return text[:start] + self.display_entity(entity) + text[end:]

        annotated_text = text[:]
        for identifer, entity in enumerate(entities):
            entity.identifier = identifer + 1
            annotated_text = insert_entity(annotated_text, entity)

        return EntityAnnotationResults(text, annotated_text, entities)

class LabelOnlyEntityAnnotator(EntityAnnotator):
    def display_entity(self, entity: Entity) -> str:
        return f'<{entity.label}>{entity.text}</{entity.label}>'

class HtmlEntityAnnotator(EntityAnnotator):
    def display_entity(self, entity: Entity) -> str:
        key = re.sub(r' ', '-', entity.label)
        return f'<span class="entity lb-{key}">' + \
            f'<span class="label">{entity.label}</span>' + \
            f'{entity.text}' + \
            '</span>'
    