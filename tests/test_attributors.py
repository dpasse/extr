import os
import sys
import re

sys.path.insert(0, os.path.join('../src'))

from extr import RegEx, RegExLabel
from extr.entities import create_entity_extractor, \
                          EntityAttributor, \
                          AttributeToApply, \
                          AttributeApplications, \
                          AttributeSetup


def test_apply_attribute_to_entity():
    regex_labels = [
        RegExLabel('PERSON', [
            RegEx([r'ted'], re.IGNORECASE)
        ]),
        RegExLabel('POSITION', [
            RegEx([r'pitcher'], re.IGNORECASE)
        ]),
    ]

    text = 'Ted is not a Pitcher.'
    extractor = create_entity_extractor(regex_labels)
    entities = extractor.get_entities(text)

    attributor = EntityAttributor(
        attribute_name='ctypes',
        settings = [
            AttributeToApply(
                'NEGATIVE',
                applications=[
                    AttributeApplications(
                        entities=['POSITION'],
                        setups=[
                            AttributeSetup(before=r' not a ')
                        ]
                    )
                ]
            )
        ]
    )

    entities = attributor.set_attributes(text, entities)

    assert 'NEGATIVE' in entities[0].attributes['ctypes']
    assert not 'ctypes' in entities[1].attributes
