from typing import Generic, Protocol, TypeVar

from maxo.routing.ctx import Ctx
from maxo.routing.filters.always import AlwaysTrueFilter
from maxo.routing.interfaces.filter import Filter
from maxo.routing.interfaces.handler import Handler
from maxo.routing.signals.base import BaseSignal

_SignalT = TypeVar("_SignalT", bound=BaseSignal)
_ReturnT_co = TypeVar("_ReturnT_co", covariant=True)


class SignalHandlerFn(Protocol[_SignalT, _ReturnT_co]):
    async def __call__(self, ctx: Ctx[_SignalT]) -> _ReturnT_co: ...


class SignalHandler(
    Handler[_SignalT, _ReturnT_co],
    Generic[_SignalT, _ReturnT_co],
):
    __slots__ = (
        "_filter",
        "_handler_fn",
    )

    def __init__(
        self,
        handler_fn: SignalHandlerFn[_SignalT, _ReturnT_co],
        filter: Filter[_SignalT] | None = None,
    ) -> None:
        if filter is None:
            filter = AlwaysTrueFilter()

        self._filter = filter
        self._handler_fn = handler_fn

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(handler_fn={self._handler_fn}, filter={self._filter})"

    async def execute_filter(self, ctx: Ctx[_SignalT]) -> bool:
        return await self._filter.execute(ctx.update, ctx)

    async def execute(self, ctx: Ctx[_SignalT]) -> _ReturnT_co:
        return await self._handler_fn(ctx=ctx)
