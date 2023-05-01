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
class AttributeApplications:
    entities: List[str]
    setups: List[AttributeSetup]

    def get_expression(self):
        expressions = []
        for setup in self.setups:
            expression = setup.before if setup.before else ''
            expression += r'(##ENTITY_(?:' + '|'.join(self.entities) + r')_\d+##)'
            if setup.after:
                expression += setup.after

            expressions.append(expression)

        return SlimRegEx(expressions)

@dataclass
class AttributeToApply:
    name: str
    applications: List[AttributeApplications]

class EntityAttributor:
    def __init__(self, attribute_name: str, settings: List[AttributeToApply]) -> None:
        self._attribute_name = attribute_name
        self._settings = settings

    def set_attributes(self, text: str, entities: List[Entity]) -> List[Entity]:
        annotated_text = EntityAnnotator().annotate(text, entities).annotated_text

        mappings = Query(entities).todict(str)
        for setting in self._settings:
            for application in setting.applications:
                for match in application.get_expression().findall(annotated_text):
                    groups = list(match.groups())
                    key = Query(groups) \
                        .find(lambda g: g.startswith('##ENTITY_'))

                    if key:
                        mappings[key].add_attribute(
                            self._attribute_name,
                            setting.name
                        )

        return list(mappings.values())
