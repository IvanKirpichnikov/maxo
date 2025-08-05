from typing import Any, Generic, TypeVar

from maxo.routing.interfaces.filter import Filter
from maxo.routing.updates.base import BaseUpdate

_UpdateT = TypeVar("_UpdateT", bound=BaseUpdate)


class BaseFilter(Filter[_UpdateT], Generic[_UpdateT]):
    def __and__(self, other: "Filter[_UpdateT] | Any") -> "Filter[_UpdateT]":
        if not isinstance(other, Filter):
            return NotImplemented

        from maxo.routing.filters.logic import AndFilter

        return AndFilter(self, other)

    def __or__(self, other: "Filter[_UpdateT] | Any") -> "Filter[_UpdateT]":
        if not isinstance(other, Filter):
            return NotImplemented

        from maxo.routing.filters.logic import OrFilter

        return OrFilter(self, other)

    def __invert__(self) -> "Filter[_UpdateT]":
        from maxo.routing.filters.logic import InvertFilter

        return InvertFilter(self)
