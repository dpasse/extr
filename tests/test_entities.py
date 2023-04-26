import os
import sys
import re

sys.path.insert(0, os.path.join('../src'))

from extr import RegEx, RegExLabel, Entity, Location
from extr.entities import EntityExtractor, EntityAnnotator, HtmlEntityAnnotator

def test_get_entities():
    extractor = EntityExtractor([
        RegExLabel('PERSON', [
            RegEx([r'ted'], re.IGNORECASE)
        ]),
        RegExLabel('POSITION', [
            RegEx([r'pitcher'], re.IGNORECASE)
        ]),
    ])

    entities = extractor.get_entities('Ted is a Pitcher.')

    assert len(entities) == 2

def test_get_entities_with_knowledge():
    kb = {
        'PERSON': [
            'Ted'
        ]
    }

    extractor = EntityExtractor(
        [
            RegExLabel('POSITION', [
                RegEx([r'pitcher'], re.IGNORECASE)
            ]),
        ],
        kb
    )

    entities = extractor.get_entities('Ted is a Pitcher.')

    assert len(entities) == 2

def test_annotate():
    entities = [
        Entity('POSITION', 'Pitcher', Location(9, 16), 1),
        Entity('PERSON', 'Ted', Location(0, 3), 2)
    ]

    annotations = EntityAnnotator().annotate('Ted is a Pitcher.', entities)

    assert annotations.original_text == 'Ted is a Pitcher.'
    assert annotations.annotated_text == '##ENTITY_PERSON_2## is a ##ENTITY_POSITION_1##.'

def test_html_annotate():
    entities = [
        Entity('POSITION', 'Pitcher', Location(9, 16), 1),
        Entity('PERSON', 'Ted', Location(0, 3), 2)
    ]

    annotations = HtmlEntityAnnotator().annotate('Ted is a Pitcher.', entities)

    assert annotations.original_text == 'Ted is a Pitcher.'
    assert annotations.annotated_text == '<span class="entity lb-PERSON"><span class="label">PERSON</span>Ted</span> is a <span class="entity lb-POSITION"><span class="label">POSITION</span>Pitcher</span>.'
