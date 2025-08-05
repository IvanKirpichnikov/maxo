from collections.abc import Callable, MutableSequence
from typing import Any, Coroutine, Sequence, TypeVar, cast

from maxo.routing.ctx import Ctx
from maxo.routing.filters.always import AlwaysTrueFilter
from maxo.routing.interfaces.filter import Filter
from maxo.routing.interfaces.handler import Handler
from maxo.routing.interfaces.observer import Observer, ObserverState
from maxo.routing.middlewares.manager import MiddlewareManagerFacade
from maxo.routing.observers.state import EmptyObserverState
from maxo.routing.sentinels import UNHANDLED
from maxo.routing.updates.base import BaseUpdate

_UpdateT = TypeVar("_UpdateT", bound=BaseUpdate)
_ReturnT_co = TypeVar("_ReturnT_co", covariant=True)

_HandlerT = TypeVar("_HandlerT", bound=Handler[Any, Any])
_HandlerFnT = TypeVar("_HandlerFnT", bound=Callable[..., Coroutine[Any, Any, Any]])


class BaseObserver(Observer[_UpdateT, _HandlerT, _HandlerFnT]):
    _filter: Filter[_UpdateT]
    _handlers: MutableSequence[_HandlerT]
    _middleware: MiddlewareManagerFacade[_UpdateT]
    __state: ObserverState

    __slots__ = (
        "_filter",
        "_inner_middleware",
        "_outer_middleware",
    )

    def __init__(self) -> None:
        self._handlers = []
        self._filter = AlwaysTrueFilter()
        self._middleware = MiddlewareManagerFacade()

        self.__state = EmptyObserverState()

    @property
    def _state(self) -> ObserverState:
        return self.__state

    @_state.setter
    def _state(self, value: ObserverState) -> None:
        self.__state = value

    @property
    def handlers(self) -> Sequence[_HandlerT]:
        return self._handlers

    @property
    def middleware(self) -> MiddlewareManagerFacade[_UpdateT]:
        return self._middleware

    def __call__(
        self,
        filter: Filter[_UpdateT] | None = None,
    ) -> Callable[[_HandlerFnT], _HandlerFnT]:
        def wrapper(handler_fn: _HandlerFnT) -> _HandlerFnT:
            return self.handler(handler_fn, filter)

        return wrapper

    def filter(self, filter: Filter[_UpdateT]) -> None:
        self._state.ensure_add_filter()

        self._filter = filter

    async def execute_filter(self, ctx: Ctx[_UpdateT]) -> bool:
        return await self._filter.execute(ctx.update, ctx)

    async def handler_lookup(self, ctx: Ctx[_UpdateT]) -> Any:
        for handler in self._handlers:
            if await handler.execute_filter(ctx):
                return await self.execute_handler(ctx, handler)

        return UNHANDLED

    async def execute_handler(
        self,
        ctx: Ctx[_UpdateT],
        handler: _HandlerT,
    ) -> _ReturnT_co:
        chain_middlewares = self.middleware.inner._make_chain(handler.execute)
        return cast("_ReturnT_co", await chain_middlewares(ctx))
