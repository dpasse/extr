from typing import List, Optional
from dataclasses import dataclass

from .annotator import EntityAnnotator
from ..models import Entity
from ..utils import Query
from ..regexes import SlimRegEx


@dataclass
class AttributeSetup:
    before: Optional[str] = None
    after: Optional[str] = None

@dataclass
class AttributeToApply:
    name: str
    entity_label: str

    setups: List[AttributeSetup]

class EntityAttributor:
    def __init__(self, settings: List[AttributeToApply]) -> None:
        self._settings = settings

    def set(self, text: str, entities: List[Entity]) -> List[Entity]:
        annotated_text = EntityAnnotator().annotate(text, entities).annotated_text

        mappings = Query(entities).todict(str)
        for setting in self._settings:
            for attribute_setup in setting.setups:
                expression = attribute_setup.before if attribute_setup.before else ''
                expression += r'(##ENTITY_' + setting.entity_label + r'_\d+##)'
                if attribute_setup.after:
                    expression += attribute_setup.after

                for match in SlimRegEx([expression]).findall(annotated_text):
                    groups = list(match.groups())
                    key = Query(groups) \
                        .find(lambda g: g.startswith('##ENTITY_'))

                    if key:
                        mappings[key].add_attribute(
                            'types',
                            setting.name
                        )

        return list(mappings.values())
