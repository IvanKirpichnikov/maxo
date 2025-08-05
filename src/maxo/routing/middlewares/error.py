from typing import Any

from maxo.routing.ctx import Ctx
from maxo.routing.interfaces.middleware import Middleware, NextMiddleware
from maxo.routing.interfaces.router import Router
from maxo.routing.sentinels import UNHANDLED
from maxo.routing.signals.exception import ExceptionEvent


class ErrorMiddleware(Middleware[Any]):
    __slots__ = ("_router",)

    def __init__(self, router: Router) -> None:
        self._router = router

    async def execute(
        self,
        update: Any,
        ctx: Ctx[Any],
        next: NextMiddleware[Any],
    ) -> Any:
        try:
            return await next(ctx)
        except Exception as error:
            exception_event = ExceptionEvent(
                error=error,
                update=update,
            )
            ctx = Ctx.factory(exception_event, ctx.raw_data)
            result = await self._router.trigger(ctx)
            if result is UNHANDLED:
                raise
            return result
