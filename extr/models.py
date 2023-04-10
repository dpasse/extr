from typing import List, Dict, Any

from dataclasses import dataclass, field


NOT_DEFINED_FLAG: int = -1

@dataclass()
class Entity:
    label: str
    text: str
    start: int
    end: int
    identifer: int = NOT_DEFINED_FLAG
    token_id: int = NOT_DEFINED_FLAG
    attributes: Dict[str, Any] = field(default_factory=dict)

    def __repr__(self) -> str:
        return f'<Entity label="{self.label}" text="{self.text}" span=({self.start}, {self.end})>'

    def __str__(self) -> str:
        return f'##ENTITY_{self.label}_{self.identifer}##'

@dataclass(frozen=True)
class EntityAnnotationResults:
    original_text: str
    annotated_text: str
    entities: List[Entity]

    @property
    def entity_lookup(self):
        return { str(entity): entity for entity in self.entities }

@dataclass(frozen=True)
class Relation:
    label: str
    e1: Entity
    e2: Entity

    def __repr__(self) -> str:
        return f'<Relation e1="{self.e1.text}" r="{self.label}" e2="{self.e2.text}">'
