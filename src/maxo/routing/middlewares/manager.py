from collections.abc import Awaitable, Callable, MutableSequence
from typing import Any, Generic, TypeVar, cast

from maxo.routing.ctx import Ctx
from maxo.routing.interfaces.middleware import Middleware, NextMiddleware
from maxo.routing.middlewares.state import EmptyMiddlewareManagerState, MiddlewareManagerState
from maxo.routing.updates.base import BaseUpdate

_ReturnT = TypeVar("_ReturnT")
_UpdateT = TypeVar("_UpdateT", bound=BaseUpdate)


def _partial_middleware(
    middleware: Middleware[_UpdateT],
    next: NextMiddleware[_UpdateT],
) -> NextMiddleware[_UpdateT]:
    async def wrapper(ctx: Ctx[_UpdateT]) -> Any:
        return await middleware.execute(
            ctx=ctx,
            update=ctx.update,
            next=next,
        )

    return wrapper


class MiddlewareManager(Generic[_UpdateT]):
    _middlewares: MutableSequence[Middleware[_UpdateT]]

    _state: MiddlewareManagerState

    __slots__ = ("_middlewares", "_state")

    def __init__(self) -> None:
        self._middlewares = []

        self._state = EmptyMiddlewareManagerState()

    def __call__(self, *middlewares: Middleware[_UpdateT]) -> None:
        self.add(*middlewares)

    def add(self, *middlewares: Middleware[_UpdateT]) -> None:
        self._state.ensure_add_middleware()
        self._middlewares.extend(middlewares)

    def _make_chain(
        self,
        trigger: Callable[[Ctx[_UpdateT]], Awaitable[_ReturnT]],
    ) -> NextMiddleware[_UpdateT]:
        middleware = cast("NextMiddleware[_UpdateT]", trigger)

        for m in reversed(self._middlewares):
            middleware = _partial_middleware(m, middleware)

        return middleware


class MiddlewareManagerFacade(Generic[_UpdateT]):
    _inner: MiddlewareManager[_UpdateT]
    _outer: MiddlewareManager[_UpdateT]

    __slots__ = (
        "_inner",
        "_outer",
    )

    def __init__(self) -> None:
        self._inner = MiddlewareManager()
        self._outer = MiddlewareManager()

    @property
    def inner(self) -> MiddlewareManager[_UpdateT]:
        return self._inner

    @property
    def outer(self) -> MiddlewareManager[_UpdateT]:
        return self._outer
