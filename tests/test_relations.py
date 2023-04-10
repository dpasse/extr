import os
import sys

sys.path.insert(0, os.path.join('../src'))

from extr_nlp import Entity, EntityAnnotationResults, RegExRelationLabelBuilder, RelationExtractor


def test_get_relations():
    annotations = EntityAnnotationResults(
        'Ted is a Pitcher.',
        '##ENTITY_PERSON_2## is a ##ENTITY_POSITION_1##.',
        [
            Entity('POSITION', 'Pitcher', 9, 16, 1),
            Entity('PERSON', 'Ted', 0, 3, 2)
        ]
    )

    ## define relationship between PERSON and POSITION    
    relationship = RegExRelationLabelBuilder('is_a') \
        .add_e1_to_e2(
            'PERSON', ## e1
            [
                ## define how the relationship exists in nature
                r'\s+is\s+a\s+',
            ],
            'POSITION' ## e2
        ) \
        .build()
        
    relations_to_extract = [relationship]

    relations = RelationExtractor(relations_to_extract).extract(annotations)
    
    assert len(relations) == 1
    assert relations[0].e1.text == 'Ted'
    assert relations[0].e2.text == 'Pitcher'
    assert relations[0].label == 'is_a'
    