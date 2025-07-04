from abc import abstractmethod
from typing import Any, Protocol, TypeVar, runtime_checkable

from maxo.kerno.routing.ctx import Ctx
from maxo.kerno.types.updates.base import BaseUpdate

U = TypeVar("U", bound=BaseUpdate)


@runtime_checkable
class Filter(Protocol[U]):
    __slots__ = ()

    @abstractmethod
    async def execute(
        self,
        update: U,
        ctx: Ctx[U],
    ) -> bool:
        raise NotImplementedError

    def __and__(self, other: "Filter[U] | Any") -> "Filter[U]":
        if not isinstance(other, Filter):
            return NotImplemented

        from maxo.kerno.routing.filters.logic import AndFilter

        return AndFilter(self, other)

    def __or__(self, other: "Filter[U] | Any") -> "Filter[U]":
        if not isinstance(other, Filter):
            return NotImplemented

        from maxo.kerno.routing.filters.logic import OrFilter

        return OrFilter(self, other)

    def __xor__(self, other: "Filter[U] | Any") -> "Filter[U]":
        if not isinstance(other, Filter):
            return NotImplemented

        from maxo.kerno.routing.filters.logic import XorFilter

        return XorFilter(self, other)

    def __invert__(self) -> "Filter[U]":
        from maxo.kerno.routing.filters.logic import InvertFilter

        return InvertFilter(self)
