from collections.abc import Callable, MutableSequence
from typing import Any, Generic, ParamSpec, TypeVar, cast

from maxo.routing.dispatcher.ctx import Ctx
from maxo.routing.dispatcher.handler import Handler, HandlerFn
from maxo.routing.dispatcher.sentinels import UNHANDLED
from maxo.routing.filters.base import Filter
from maxo.routing.middlewares.manager import MiddlewareManager
from maxo.types.updates.base import BaseUpdate

T = TypeVar("T")
P = ParamSpec("P")
U = TypeVar("U", bound=BaseUpdate)


class UpdateObserver(Generic[U]):
    outer_middleware: MiddlewareManager[U]
    inner_middleware: MiddlewareManager[U]

    _handlers: MutableSequence[Handler[U, Any, Any]]

    def __init__(self) -> None:
        self._handlers = []

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
        self._handlers.append(handler)
        return handler_fn

    async def search_handler(self, ctx: Ctx[U]) -> Any:
        for handler in self._handlers:
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
