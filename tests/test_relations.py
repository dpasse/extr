import os
import sys

sys.path.insert(0, os.path.join('..'))

from extr import Entity, EntityAnnotationResults, RegExRelationLabel, RelationExtractor


def test_get_relations():
    annotations = EntityAnnotationResults(
        'Ted is a Pitcher.',
        '##ENTITY_PERSON_2## is a ##ENTITY_POSITION_1##.',
        [
            Entity('POSITION', 'Pitcher', 9, 16, 1),
            Entity('PERSON', 'Ted', 0, 3, 2)
        ]
    )

    relationship = RegExRelationLabel('is_a')
    relationship.add_e1_to_e2(
        'PERSON',
        [r'\s+is\s+a\s+'],
        'POSITION'
    )

    relations = RelationExtractor([relationship]).extract(annotations)
    
    assert len(relations) == 1
    assert relations[0].e1.text == 'Ted'
    assert relations[0].e2.text == 'Pitcher'
    assert relations[0].label == 'is_a'
    