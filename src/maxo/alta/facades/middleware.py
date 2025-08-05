from collections.abc import Mapping
from typing import Any, final

from maxo.alta.facades.updates.base import BaseUpdateFacade
from maxo.alta.facades.updates.message_callback import MessageCallbackFacade
from maxo.alta.facades.updates.message_created import MessageCreatedFacade
from maxo.routing.ctx import Ctx
from maxo.routing.interfaces.middleware import Middleware, NextMiddleware
from maxo.routing.signals.update import Update
from maxo.routing.updates.base import BaseUpdate
from maxo.routing.updates.message_callback import MessageCallback
from maxo.routing.updates.message_created import MessageCreated

_FACEDS_MAP: Mapping[type[Any], type[BaseUpdateFacade[Any]]] = {
    MessageCreated: MessageCreatedFacade,
    MessageCallback: MessageCallbackFacade,
}


class FacadeMiddleware(Middleware[Update[Any]]):
    @final
    async def execute(
        self,
        update: Update[Any],
        ctx: Ctx[Update[Any]],
        next: NextMiddleware[Update[Any]],
    ) -> Any:
        facade = self._facade_cls_factory(type(update.update))
        ctx.facade = facade(ctx.bot, update.update)

        return await next(ctx)

    def _facade_cls_factory(
        self,
        update_tp: type[BaseUpdate],
    ) -> type[BaseUpdateFacade[Any]]:
        return _FACEDS_MAP[update_tp]
