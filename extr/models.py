from typing import List

from dataclasses import dataclass


@dataclass()
class Entity:
    label: str
    text: str
    start: int
    end: int
    identifer: int = 0

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
