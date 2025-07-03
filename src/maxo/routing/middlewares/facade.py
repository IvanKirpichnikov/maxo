from collections.abc import Mapping
from typing import Any

from maxo.alta.facades.updates.base import BaseUpdateFacade
from maxo.alta.facades.updates.message_callback import MessageCallbackFacade
from maxo.alta.facades.updates.message_created import MessageCreatedFacade
from maxo.routing.dispatcher.ctx import Ctx
from maxo.routing.middlewares.base import Middleware, NextMiddleware
from maxo.types.updates.message_callback import MessageCallback
from maxo.types.updates.message_created import MessageCreated
from maxo.types.updates.update import Update

_FACEDS_MAP: Mapping[type[Any], type[BaseUpdateFacade[Any]]] = {
    MessageCreated: MessageCreatedFacade,
    MessageCallback: MessageCallbackFacade,
}


class FacadeMiddleware(Middleware[Update[Any]]):
    async def execute(
        self,
        update: Update[Any],
        ctx: Ctx[Update[Any]],
        next: NextMiddleware[Update[Any]],
    ) -> Any:
        facade = _FACEDS_MAP.get(type(update.update))
        if facade is not None:
            ctx["facade"] = facade(ctx.bot, update.update)

        return await next(ctx)
