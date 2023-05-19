import os
import sys
import re

sys.path.insert(0, os.path.join('../src'))

from extr import RegEx, RegExLabel, Entity, Location
from extr.entities import create_entity_extractor, EntityAnnotator, HtmlEntityAnnotator

def test_get_entities():
    regex_labels = [
        RegExLabel('PERSON', [
            RegEx([r'ted'], re.IGNORECASE)
        ]),
        RegExLabel('POSITION', [
            RegEx([r'pitcher'], re.IGNORECASE)
        ]),
    ]

    extractor = create_entity_extractor(regex_labels)
    entities = extractor.get_entities('Ted is a Pitcher.')

    assert len(entities) == 2

def test_get_entities_with_knowledge():
    extractor = create_entity_extractor(
        regex_labels=[
            RegExLabel('POSITION', [
                RegEx([r'pitcher'], re.IGNORECASE)
            ]),
        ],
        kb={
            'PERSON': [
                'Ted'
            ]
        }
    )

    entities = extractor.get_entities('Ted is a Pitcher.')

    assert len(entities) == 2

def test_annotate():
    entities = [
        Entity(1, 'POSITION', 'Pitcher', Location(9, 16), 1),
        Entity(2, 'PERSON', 'Ted', Location(0, 3), 2)
    ]

    annotated_text = EntityAnnotator().annotate('Ted is a Pitcher.', entities)

    assert annotated_text == '##ENTITY_PERSON_2## is a ##ENTITY_POSITION_1##.'

def test_html_annotate():
    entities = [
        Entity(1, 'POSITION', 'Pitcher', Location(9, 16), 1),
        Entity(2, 'PERSON', 'Ted', Location(0, 3), 2)
    ]

    annotated_text = HtmlEntityAnnotator().annotate('Ted is a Pitcher.', entities)

    assert annotated_text == '<span class="entity lb-PERSON"><span class="label">PERSON</span>Ted</span> is a <span class="entity lb-POSITION"><span class="label">POSITION</span>Pitcher</span>.'
