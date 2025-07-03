from typing import Generic, TypeVar, final

from maxo.dispatcher.ctx import Ctx
from maxo.filters.base import Filter
from maxo.types.updates.base import BaseUpdate

U = TypeVar("U", bound=BaseUpdate)


@final
class AndFilter(Filter[U], Generic[U]):
    def __init__(
        self,
        lgh: Filter[U],
        rgh: Filter[U],
    ) -> None:
        self._lgh = lgh
        self._rgh = rgh

    async def execute(self, ctx: Ctx[U]) -> bool:
        return await self._lgh.execute(ctx) and await self._rgh.execute(ctx)


@final
class OrFilter(Filter[U], Generic[U]):
    def __init__(
        self,
        lgh: Filter[U],
        rgh: Filter[U],
    ) -> None:
        self._lgh = lgh
        self._rgh = rgh

    async def execute(self, ctx: Ctx[U]) -> bool:
        return await self._lgh.execute(ctx) or await self._rgh.execute(ctx)


@final
class XorFilter(Filter[U], Generic[U]):
    def __init__(
        self,
        lgh: Filter[U],
        rgh: Filter[U],
    ) -> None:
        self._lgh = lgh
        self._rgh = rgh

    async def execute(self, ctx: Ctx[U]) -> bool:
        return await self._lgh.execute(ctx) != await self._rgh.execute(ctx)


@final
class InvertFilter(Filter[U], Generic[U]):
    def __init__(
        self,
        filter: Filter[U],
    ) -> None:
        self._filter = filter

    async def execute(self, ctx: Ctx[U]) -> bool:
        return not await self._filter.execute(ctx)
