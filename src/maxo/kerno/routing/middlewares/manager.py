from collections.abc import Awaitable, Callable, MutableSequence
from typing import Any, Generic, TypeVar

from maxo.kerno.routing.ctx import Ctx
from maxo.kerno.routing.middlewares.base import Middleware, NextMiddleware
from maxo.kerno.types.updates.base import BaseUpdate

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
    middlewares: MutableSequence[Middleware[U]]

    __slots__ = ("middlewares",)

    def __init__(self) -> None:
        self.middlewares = []

    def __call__(self, *middlewares: Middleware[U]) -> None:
        self.middlewares.extend(middlewares)

    def make_chain(
        self,
        trigger: Callable[[Ctx[U]], Awaitable[T]],
    ) -> NextMiddleware[U]:
        middleware = call_trigger_middleware(trigger)
        for m in reversed(self.middlewares):
            middleware = partial_middleware(m, middleware)

        return middleware
