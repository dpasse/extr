import re
from ..models import Relation, Entity


class RelationAnnotator:
    def display_entity(self, entity: Entity, position: int) -> str:
        return f'<e{str(position)}>{entity.text}</e{str(position)}>'

    def annotate(self, text: str, relation: Relation, offset = 0) -> str:
        annotated_text = text[:]

        e1 = relation.e1
        e1_start = e1.location.start - offset
        e1_end = e1.location.end - offset

        e2 = relation.e2
        e2_start = e2.location.start - offset
        e2_end = e2.location.end - offset

        if e1_end < e2_start:
            return annotated_text[:e1_start] + \
                self.display_entity(e1, 1) + \
                annotated_text[e1_end:e2_start] + \
                self.display_entity(e2, 2) + \
                annotated_text[e2_end:]

        return annotated_text[:e2_start] + \
            self.display_entity(e2, 2) + \
            annotated_text[e2_end:e1_start] + \
            self.display_entity(e1, 1) + \
            annotated_text[e1_end:]

class RelationAnnotatorWithEntityType(RelationAnnotator):
    def display_entity(self, entity: Entity, position: int) -> str:
        return f'<e{str(position)}:{entity.label}>{entity.text}</e{str(position)}:{entity.label}>'

class HtmlRelationAnnotator(RelationAnnotator):
    def display_entity(self, entity: Entity, position: int) -> str:
        key = re.sub(r' ', '-', entity.label)
        return f'<span class="entity lb-{key} e{position}">' + \
            f'<span class="label">{entity.label}</span>' + \
            f'{entity.text}' + \
            '</span>'
