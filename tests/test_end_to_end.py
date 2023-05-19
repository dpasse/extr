import os
import sys
import re
import pytest

sys.path.insert(0, os.path.join('../src'))

from extr import RegEx, RegExLabel
from extr.entities import EntityExtractor, EntityAnnotator
from extr.relations import RelationExtractor, RegExRelationLabelBuilder


@pytest.mark.skip
def test_end_to_end():
    text = 'Walk; Mountcastle to 3B; Odor to 2B'

    entity_extractor = EntityExtractor([
        RegExLabel('PLAYER', [
            RegEx([
                r'\b([A-Z]\w+)(?=\s+to\b)'
            ])
        ]),
        RegExLabel('BASE', [
            RegEx([
                r'([123]B)\b'
            ])
        ]),
        RegExLabel('EVENT', [
            RegEx(
                [
                    r'\b(Walk|Single)\b'
                ],
                re.IGNORECASE
            )
        ]),
    ])

    entities = entity_extractor.get_entities(text)
    print(entities)
    assert len(entities) == 5

    player_to_base_relationship = RegExRelationLabelBuilder('is_on') \
        .add_e1_to_e2(
            'PLAYER', ## e1
            [
                ## define how the relationship exists in nature
                r'\s+to\s+',
            ],
            'BASE' ## e2
        ) \
        .build()

    relations_to_extract = [
        player_to_base_relationship
    ]

    annotations = EntityAnnotator().annotate(text, entities)
    relations = RelationExtractor(relations_to_extract).extract(annotations)

    print(relations)
    assert len(relations) == 2
