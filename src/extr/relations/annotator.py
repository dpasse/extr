from ..models import Relation


class RelationAnnotator:
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
                f'<e1>{e1.text}</e1>' + \
                annotated_text[e1_end:e2_start] + \
                f'<e2>{e2.text}</e2>' + \
                annotated_text[e2_end:]

        return annotated_text[:e2_start] + \
            f'<e2>{e2.text}</e2>' + \
            annotated_text[e2_end:e1_start] + \
            f'<e1>{e1.text}</e1>' + \
            annotated_text[e1_end:]
        