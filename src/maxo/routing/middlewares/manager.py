from collections.abc import Awaitable, Callable, MutableSequence
from typing import Any, Generic, TypeVar

from maxo.routing.dispatcher.ctx import Ctx
from maxo.routing.middlewares.base import Middleware, NextMiddleware
from maxo.types.updates.base import BaseUpdate

T = TypeVar("T")
U = TypeVar("U", bound=BaseUpdate)


def call_trigger_middleware(
    trigger: Callable[[Ctx[U]], Awaitable[T]],
) -> NextMiddleware[U]:
    async def wrapper(ctx: Ctx[U]) -> T:
        return await trigger(ctx)

    return wrapper


def partial_middleware(middleware: Middleware[U], next: NextMiddleware[U]) -> NextMiddleware[U]:
    async def wrapper(ctx: Ctx[U]) -> Any:
        return await middleware.execute(
            ctx=ctx,
            update=ctx.update,
            next=next,
        )

    return wrapper


class MiddlewareManager(Generic[U]):
    _middlewares: MutableSequence[Middleware[U]]

    def __init__(self) -> None:
        self._middlewares = []

    def __call__(self, *middlewares: Middleware[U]) -> None:
        self._middlewares.extend(middlewares)

    def _extend_manager(self, manager: "MiddlewareManager[U]") -> None:
        self._middlewares.extend(manager._middlewares)

    def make_chain(
        self,
        trigger: Callable[[Ctx[U]], Awaitable[T]],
    ) -> NextMiddleware[U]:
        middleware = call_trigger_middleware(trigger)
        for m in reversed(self._middlewares):
            middleware = partial_middleware(m, middleware)

        return middleware
