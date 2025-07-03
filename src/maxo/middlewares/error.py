from typing import Any

from maxo.dispatcher.ctx import Ctx
from maxo.dispatcher.router import Router
from maxo.dispatcher.sentinels import UNHANDLED
from maxo.middlewares.base import Middleware, NextMiddleware
from maxo.types.updates.error import ErrorEvent


class ErrorMiddleware(Middleware[Any]):
    def __init__(self, router: Router) -> None:
        self._router = router

    async def execute(
        self,
        ctx: Ctx[Any],
        update: Any,
        next: NextMiddleware[Any],
    ) -> Any:
        try:
            return await next(ctx)
        except Exception as error:
            error_event_update = ErrorEvent(
                error=error,
                update=update,
            )
            ctx = Ctx(error_event_update, ctx.data)
            result = await self._router.trigger(ctx)
            if result is UNHANDLED:
                raise
            return result
