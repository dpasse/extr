import os
import sys
import re

sys.path.insert(0, os.path.join('../src'))

from extr import RegEx, RegExLabel, Entity, Location
from extr.entities import EntityExtractor, EntityAnnotator

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

def test_annotate():
    entities = [
        Entity('POSITION', 'Pitcher', Location(9, 16), 1),
        Entity('PERSON', 'Ted', Location(0, 3), 2)
    ]

    annotations = EntityAnnotator().annotate('Ted is a Pitcher.', entities)

    assert annotations.original_text == 'Ted is a Pitcher.'
    assert annotations.annotated_text == '##ENTITY_PERSON_2## is a ##ENTITY_POSITION_1##.'
