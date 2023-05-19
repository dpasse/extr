from typing import List
import re

from ..models import Entity


class EntityAnnotator:
    def display_entity(self, entity: Entity) -> str:
        return str(entity)

    def annotate(self, text: str, entities: List[Entity]) -> str:
        def insert_entity(text: str, entity: Entity) -> str:
            start = entity.start
            end = entity.end
            return text[:start] + self.display_entity(entity) + text[end:]

        annotated_text = text[:]
        for entity in entities:
            annotated_text = insert_entity(annotated_text, entity)

        return annotated_text

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
    