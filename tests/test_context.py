import os
import sys
import re

sys.path.insert(0, os.path.join('../src'))

from extr import RegEx, RegExLabel
from extr.entities import create_entity_extractor
from extr.entities.context import ConText, ConTextRule, ConTextRuleGroup, DirectionType


regex_labels=[
    RegExLabel(
        'LEFT_NEGATIVE',
        regexes=[
            RegEx([r'is ruled out'], flags=re.IGNORECASE)
        ]
    ),
    RegExLabel(
        'HISTORY_RIGHT',
        regexes=[
            RegEx([r'history of'], flags=re.IGNORECASE)
        ]
    ),
    RegExLabel(
        'INFECTION',
        regexes=[
            RegEx([r'pneumonia'], flags=re.IGNORECASE)
        ]
    ),
]

rules = [
    ConTextRule(
        'NEGATED',
        ['RIGHT_NEGATIVE'],
        direction=DirectionType.RIGHT
    ),
    ConTextRule(
        'NEGATED',
        ['LEFT_NEGATIVE'],
        direction=DirectionType.LEFT
    ),
    ConTextRule(
        'HISTORICAL',
        ['HISTORY_RIGHT'],
        direction=DirectionType.RIGHT
    ),
    ConTextRule(
        'HISTORICAL',
        ['HISTORY_LEFT'],
        direction=DirectionType.LEFT
    ),
    ConTextRule(
        'HYPOTHETICAL',
        ['HYPOTHETICAL_RIGHT'],
        direction=DirectionType.RIGHT
    ),
    ConTextRule(
        'HYPOTHETICAL',
        ['HYPOTHETICAL_LEFT'],
        direction=DirectionType.LEFT
    )
]

def test_contextor_historical_right_1():
    text = 'Past history of pneumonia.'
    entity_extractor = create_entity_extractor(regex_labels=regex_labels)

    contextor = ConText(
        rule_grouping=ConTextRuleGroup(
            rules=rules
        ),
        word_tokenizer=lambda _: ['Past', 'history', 'of', 'pneumonia', '.']
    )

    entities = contextor.apply(
        text,
        entity_extractor.get_entities(text)
    )

    assert len(entities) == 1
    assert list(entities[0].get_attributes_by_label('ctypes'))[0] == 'HISTORICAL'

    print(
        [
            (entity, entity.get_attributes_by_label('ctypes'))
            for entity in entities
        ]
    )
    
def test_contextor_negative_left_1():
    text = 'Pneumonia is ruled out.'
    entity_extractor = create_entity_extractor(regex_labels=regex_labels)

    contextor = ConText(
        rule_grouping=ConTextRuleGroup(
            rules=rules
        ),
        word_tokenizer=lambda _: ['Pneumonia', 'is', 'ruled', 'out', '.']
    )

    entities = contextor.apply(
        text,
        entity_extractor.get_entities(text)
    )

    assert len(entities) == 1
    assert list(entities[0].get_attributes_by_label('ctypes'))[0] == 'NEGATED'


    print(
        [
            (entity, entity.get_attributes_by_label('ctypes'))
            for entity in entities
        ]
    )
