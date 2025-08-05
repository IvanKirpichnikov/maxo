from abc import abstractmethod
from collections.abc import Sequence
from typing import Generic, TypeVar, final

from maxo.routing.ctx import Ctx
from maxo.routing.filters.base import BaseFilter
from maxo.routing.interfaces.filter import Filter
from maxo.routing.updates.base import BaseUpdate

_UpdateT = TypeVar("_UpdateT", bound=BaseUpdate)


class BaseLogicFilter(BaseFilter[_UpdateT], Generic[_UpdateT]):
    __slots__ = ()

    def __init__(self) -> None:
        self._inlining()

    @final
    async def execute(self, update: _UpdateT, ctx: Ctx[_UpdateT]) -> bool:
        copied_ctx = ctx.copy()

        reduce_result = await self._reduce(update, ctx)
        if reduce_result:
            ctx.merge(copied_ctx)

        return reduce_result

    @abstractmethod
    async def _reduce(self, update: _UpdateT, ctx: Ctx[_UpdateT]) -> bool:
        raise NotImplementedError

    @abstractmethod
    def _inlining(self) -> None:
        raise NotImplementedError


@final
class AndFilter(BaseLogicFilter[_UpdateT], Generic[_UpdateT]):
    _filters: Sequence[Filter[_UpdateT]]

    def __init__(
        self,
        *filters: Filter[_UpdateT],
    ) -> None:
        self._filters = filters
        super().__init__()

    async def _reduce(self, update: _UpdateT, ctx: Ctx[_UpdateT]) -> bool:
        for filter_ in self._filters:
            loop_copied_ctx = ctx.copy()

            filter_result = await filter_.execute(update, loop_copied_ctx)
            if not filter_result:
                return False

            ctx.merge(loop_copied_ctx)

        return True

    def _inlining(self) -> None:
        inlined_filters: list[Filter[_UpdateT]] = []

        for filter in self._filters:
            if isinstance(filter, AndFilter):
                inlined_filters.extend(filter._filters)
            else:
                inlined_filters.append(filter)

        self._filters = inlined_filters


@final
class OrFilter(BaseLogicFilter[_UpdateT], Generic[_UpdateT]):
    _filters: Sequence[Filter[_UpdateT]]

    def __init__(
        self,
        *filters: Filter[_UpdateT],
    ) -> None:
        self._filters = filters
        super().__init__()

    async def _reduce(self, update: _UpdateT, ctx: Ctx[_UpdateT]) -> bool:
        for filter_ in self._filters:
            loop_copied_ctx = ctx.copy()

            filter_result = await filter_.execute(update, loop_copied_ctx)
            if filter_result:
                ctx.merge(loop_copied_ctx)
                return True

        return False

    def _inlining(self) -> None:
        inlined_filters: list[Filter[_UpdateT]] = []

        for filter in self._filters:
            if isinstance(filter, OrFilter):
                inlined_filters.extend(filter._filters)
            else:
                inlined_filters.append(filter)

        self._filters = inlined_filters


@final
class InvertFilter(BaseLogicFilter[_UpdateT], Generic[_UpdateT]):
    _inlined: bool

    def __init__(
        self,
        filter_: Filter[_UpdateT],
    ) -> None:
        self._filter = filter_
        super().__init__()

    async def _reduce(self, update: _UpdateT, ctx: Ctx[_UpdateT]) -> bool:
        filter_result = await self._filter.execute(update, ctx)
        if self._inlined:
            return filter_result
        else:
            return not filter_result

    def _inlining(self) -> None:
        if isinstance(self._filter, InvertFilter):
            self._filter = self._filter._filter
            self._inlined = True
        else:
            self._inlined = False
