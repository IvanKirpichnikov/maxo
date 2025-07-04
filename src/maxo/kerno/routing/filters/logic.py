from typing import Generic, TypeVar, final

from maxo.kerno.routing.ctx import Ctx
from maxo.kerno.routing.filters.base import Filter
from maxo.kerno.types.updates.base import BaseUpdate

U = TypeVar("U", bound=BaseUpdate)


@final
class AndFilter(Filter[U], Generic[U]):
    __slots__ = ("_lgh", "_rgh")

    def __init__(
        self,
        lgh: Filter[U],
        rgh: Filter[U],
    ) -> None:
        self._lgh = lgh
        self._rgh = rgh

    async def execute(self, update: U, ctx: Ctx[U]) -> bool:
        return await self._lgh.execute(update, ctx) and await self._rgh.execute(update, ctx)


@final
class OrFilter(Filter[U], Generic[U]):
    __slots__ = ("_lgh", "_rgh")

    def __init__(
        self,
        lgh: Filter[U],
        rgh: Filter[U],
    ) -> None:
        self._lgh = lgh
        self._rgh = rgh

    async def execute(self, update: U, ctx: Ctx[U]) -> bool:
        return await self._lgh.execute(update, ctx) or await self._rgh.execute(update, ctx)


@final
class XorFilter(Filter[U], Generic[U]):
    __slots__ = ("_lgh", "_rgh")

    def __init__(
        self,
        lgh: Filter[U],
        rgh: Filter[U],
    ) -> None:
        self._lgh = lgh
        self._rgh = rgh

    async def execute(self, update: U, ctx: Ctx[U]) -> bool:
        return await self._lgh.execute(update, ctx) != await self._rgh.execute(update, ctx)


@final
class InvertFilter(Filter[U], Generic[U]):
    __slots__ = ("_filter",)

    def __init__(
        self,
        filter: Filter[U],
    ) -> None:
        self._filter = filter

    async def execute(self, update: U, ctx: Ctx[U]) -> bool:
        return not await self._filter.execute(update, ctx)
