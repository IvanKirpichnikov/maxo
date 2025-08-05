from typing import Any, Generic, Protocol, TypeVar, runtime_checkable

from maxo.routing.ctx import Ctx
from maxo.routing.filters.always import AlwaysTrueFilter
from maxo.routing.interfaces.filter import Filter
from maxo.routing.interfaces.handler import Handler
from maxo.routing.updates.base import BaseUpdate

_UpdateT = TypeVar("_UpdateT", bound=BaseUpdate)
_ReturnT_co = TypeVar("_ReturnT_co", covariant=True)

@runtime_checkable
class UpdateHandlerFn(Protocol[_UpdateT, _ReturnT_co]):
    async def __call__(self, update: _UpdateT, ctx: Ctx[_UpdateT]) -> _ReturnT_co: ...


class UpdateHandler(
    Handler[_UpdateT, _ReturnT_co],
    Generic[_UpdateT, _ReturnT_co],
):
    __slots__ = (
        "_filter",
        "_handler_fn",
    )

    def __init__(
        self,
        handler_fn: UpdateHandlerFn[_UpdateT, _ReturnT_co],
        filter: Filter[_UpdateT] | None = None,
    ) -> None:
        if filter is None:
            filter = AlwaysTrueFilter()

        self._filter = filter
        self._handler_fn = handler_fn

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(handler_fn={self._handler_fn}, filter={self._filter})"

    async def execute_filter(self, ctx: Ctx[_UpdateT]) -> bool:
        return await self._filter.execute(ctx.update, ctx)

    async def execute(self, ctx: Ctx[_UpdateT, Any]) -> _ReturnT_co:
        handler_fn_result = await self._handler_fn(update=ctx.update, ctx=ctx)
        return handler_fn_result
