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

    @property
    def actual_end(self) -> int:
        return self.end - 1

    def is_in(self: TLocation, other: TLocation) -> bool:
        return self.start >= other.start and self.start <= other.actual_end \
            or self.actual_end >= other.start and self.actual_end <= other.actual_end

    def contains(self: TLocation, other: TLocation) -> bool:
        return other.start >= self.start and other.actual_end <= self.actual_end

    def __repr__(self) -> str:
        return f'({self.start}, {self.end})'

# pylint: disable=C0103
TILocation = TypeVar('TILocation', bound='ILocation')
# pylint: enable=C0103

class ILocation:
    location: Location

    def is_in(self: TILocation, other: TILocation) -> bool:
        return self.location.is_in(other.location)

    def contains(self: TILocation, other: TILocation) -> bool:
        return self.location.contains(other.location)

@dataclass()
class Entity(ILocation):
    label: str
    text: str
    location: Location
    identifer: int = NOT_DEFINED_FLAG
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
