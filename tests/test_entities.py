import os
import sys
import re

sys.path.insert(0, os.path.join('..'))

from extr import RegEx, RegExLabel, EntityExtractor


def test_get_entities():
    annotator = EntityExtractor([
        RegExLabel('PERSON', [
            RegEx([r'ted'], re.IGNORECASE)
        ]),
        RegExLabel('POSITION', [
            RegEx([r'pitcher'], re.IGNORECASE)
        ]),
    ])

    annotations = annotator.annotate('Ted is a Pitcher.')

    assert len(annotations.entities) == 2
    assert annotations.annotated_text == '##ENTITY_PERSON_2## is a ##ENTITY_POSITION_1##.'
