from typing import Any

from maxo.kerno.routing.ctx import Ctx
from maxo.kerno.routing.middlewares.base import Middleware, NextMiddleware
from maxo.kerno.routing.routing.router import Router
from maxo.kerno.routing.sentinels import UNHANDLED
from maxo.kerno.types.updates.error import ErrorEvent


class ErrorMiddleware(Middleware[Any]):
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
            error_event_update = ErrorEvent(
                error=error,
                update=update,
            )
            ctx = Ctx(error_event_update, ctx.data)
            result = await self._router.trigger(ctx)
            if result is UNHANDLED:
                raise
            return result
