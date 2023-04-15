import os
import sys
import re
import pytest

sys.path.insert(0, os.path.join('../src'))

from extr import EntityAnnotator, RelationExtractor, EntityExtractor
from extr import RegExRelationLabelBuilder
from extr import RegEx, RegExLabel, EntityAnnotator


@pytest.mark.skip()
def test_end_to_end():
    text = 'Walk; Mountcastle to 3B; Odor to 2B'

    entity_extractor = EntityExtractor([
        RegExLabel('PERSON', [
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

    player_to_base_relationship = RegExRelationLabelBuilder('is_on') \
        .add_e1_to_e2(
            'PERSON', ## e1
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
