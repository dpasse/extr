from typing import Set, Dict, List, TypeVar, Generator

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

    def extract(self, text: str) -> str:
        return text[self.start:self.end]

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
    identifier: int = NOT_DEFINED_FLAG
    attributes: Dict[str, Set[str]] = field(default_factory=dict)

    @property
    def start(self) -> int:
        return self.location.start

    @property
    def end(self) -> int:
        return self.location.end

    def add_attribute(self, label: str, attribute: str) -> None:
        if not label in self.attributes:
            self.attributes[label] = set()

        self.attributes[label].add(attribute)

    def __repr__(self) -> str:
        return f'<Entity label="{self.label}" text="{self.text}" span={repr(self.location)}>'

    def __str__(self) -> str:
        return f'##ENTITY_{self.label}_{self.identifier}##'

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

    @property
    def key(self) -> str:
        return self.create_key(self.e1, self.e2)

    @property
    def definition(self) -> str:
        return f'r("{self.e1.label}", "{self.e2.label}")'

    def __str__(self) -> str:
        return f'r("{self.e1.text}", "{self.e2.text}") == "{self.label}"'

    def __repr__(self) -> str:
        return f'<Relation e1="{self.e1.text}" r="{self.label}" e2="{self.e2.text}">'

    @staticmethod
    def create_key(e1: Entity, e2: Entity) -> str:
        return f'{e1.identifier}_{e2.identifier}'

@dataclass(frozen=True)
class Token(ILocation):
    text: str
    location: Location
    order: int
    entities: List[Entity] = field(default_factory=lambda: [])

    def add_entity(self, entity: Entity):
        self.entities.append(entity)

    def __len__(self) -> int:
        return len(self.entities)

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return f'<Token text="{self.text}", location={repr(self.location)}, order={self.order}>'

@dataclass(frozen=True)
class TokenGroup(ILocation):
    location: Location
    sentence: str
    tokens: List[Token]

    def find_entities(self: ILocation, entities: List[Entity]) -> Generator[Entity, None, None]:
        for entity in entities:
            if self.contains(entity):
                yield entity

    def find_relations(self: ILocation, relations: List[Relation]) -> Generator[Relation, None, None]:
        for relation in relations:
            if self.contains(relation.e1) and self.contains(relation.e2):
                yield relation
