from collections.abc import Callable, MutableSequence
from typing import Any, Generic, ParamSpec, TypeVar, cast

from maxo.kerno.routing.ctx import Ctx
from maxo.kerno.routing.filters.base import Filter
from maxo.kerno.routing.middlewares.manager import MiddlewareManager
from maxo.kerno.routing.routing.handler import Handler, HandlerFn
from maxo.kerno.routing.sentinels import UNHANDLED
from maxo.kerno.types.updates.base import BaseUpdate

T = TypeVar("T")
P = ParamSpec("P")
U = TypeVar("U", bound=BaseUpdate)


class UpdateObserver(Generic[U]):
    outer_middleware: MiddlewareManager[U]
    inner_middleware: MiddlewareManager[U]

    handlers: MutableSequence[Handler[U, Any, Any]]

    def __init__(self) -> None:
        self.handlers = []

        self.inner_middleware = MiddlewareManager()
        self.outer_middleware = MiddlewareManager()

    def __call__(
        self,
        filter: Filter[U] | None = None,
    ) -> Callable[[HandlerFn[U, P, T]], HandlerFn[U, P, T]]:
        def wrapper(handler_fn: HandlerFn[U, P, T]) -> HandlerFn[U, P, T]:
            return self.add_handler(handler_fn, filter)

        return wrapper

    def add_handler(
        self,
        handler_fn: HandlerFn[U, P, T],
        filter: Filter[U] | None = None,
    ) -> HandlerFn[U, P, T]:
        handler = Handler(handler_fn, filter)
        self.handlers.append(handler)
        return handler_fn

    async def search_handler(self, ctx: Ctx[U]) -> Any:
        for handler in self.handlers:
            if await handler.execute_filter(ctx):
                return await self.execute_handler(ctx, handler)

        return UNHANDLED

    async def execute_handler(
        self,
        ctx: Ctx[U],
        handler: Handler[U, P, T],
    ) -> T:
        chain_middlewares = self.inner_middleware.make_chain(handler.execute)
        return cast("T", await chain_middlewares(ctx))
