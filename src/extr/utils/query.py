from typing import Dict, List, TypeVar, Generic, Callable, Optional
from copy import deepcopy

T = TypeVar('T')

# pylint: disable=C0103
TQuery = TypeVar('TQuery', bound='Query')
# pylint: enable=C0103

class Query(Generic[T]):
    def __init__(self: TQuery, sequence: List[T]):
        self._sequence = deepcopy(sequence)

    def __filter(self: TQuery, filter_method: Callable[[T], bool]) -> List[T]:
        return list(filter(filter_method, self._sequence))

    def filter(self: TQuery, filter_method: Callable[[T], bool]) -> TQuery:
        self._sequence = self.__filter(filter_method)
        return self

    def find(self: TQuery, find_method: Callable[[T], bool]) -> Optional[T]:
        observations = self.__filter(find_method)

        size = len(observations)
        if size > 1:
            raise Exception('Search was not unique.')

        if size == 1:
            return observations[0]

        return None

    def tolist(self: TQuery) -> List[T]:
        return self._sequence

    def todict(self: TQuery, key_method: Callable[[T], str]) -> Dict[str, T]:
        mapping: Dict[str, T] = {}
        for item in self._sequence:
            mapping[key_method(item)] = item

        return mapping
