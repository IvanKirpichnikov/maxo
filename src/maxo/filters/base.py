from abc import abstractmethod
from typing import Any, Protocol, TypeVar, runtime_checkable

from maxo.dispatcher.ctx import Ctx
from maxo.types.updates.base import BaseUpdate

U = TypeVar("U", bound=BaseUpdate)


@runtime_checkable
class Filter(Protocol[U]):
    @abstractmethod
    async def execute(self, ctx: Ctx[U]) -> bool:
        raise NotImplementedError

    def __and__(self, other: "Filter[U] | Any") -> "Filter[U]":
        if not isinstance(other, Filter):
            return NotImplemented

        from maxo.filters.logic import AndFilter

        return AndFilter(self, other)

    def __or__(self, other: "Filter[U] | Any") -> "Filter[U]":
        if not isinstance(other, Filter):
            return NotImplemented

        from maxo.filters.logic import OrFilter

        return OrFilter(self, other)

    def __xor__(self, other: "Filter[U] | Any") -> "Filter[U]":
        if not isinstance(other, Filter):
            return NotImplemented

        from maxo.filters.logic import XorFilter

        return XorFilter(self, other)

    def __invert__(self) -> "Filter[U]":
        from maxo.filters.logic import InvertFilter

        return InvertFilter(self)
