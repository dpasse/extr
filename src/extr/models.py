from typing import List, Dict, Any, TypeVar

from dataclasses import dataclass, field


NOT_DEFINED_FLAG: int = -1

# pylint: disable=C0103
TLocation = TypeVar('TLocation', bound='Location')
# pylint: enable=C0103

@dataclass(frozen=True)
class Location:
    start: int
    end: int

    def is_in(self: TLocation, other: TLocation) -> bool:
        return self.start >= other.start and self.start <= other.end \
            or self.end >= other.start and self.end <= other.end

    def contains(self: TLocation, other: TLocation) -> bool:
        return other.start >= self.start and other.end <= self.end

    def __repr__(self) -> str:
        return f'({self.start}, {self.end})'

@dataclass()
class Entity:
    label: str
    text: str
    location: Location
    identifer: int = NOT_DEFINED_FLAG
    token_id: int = NOT_DEFINED_FLAG
    attributes: Dict[str, Any] = field(default_factory=dict)

    @property
    def start(self) -> int:
        return self.location.start

    @property
    def end(self) -> int:
        return self.location.end

    def __repr__(self) -> str:
        return f'<Entity label="{self.label}" text="{self.text}" span={repr(self.location)}>'

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
