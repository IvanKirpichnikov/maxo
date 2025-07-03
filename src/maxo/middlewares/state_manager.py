from typing import Any

from maxo.dispatcher.ctx import Ctx
from maxo.middlewares.base import Middleware, NextMiddleware
from maxo.state.event_isolations.base import EventIsolation
from maxo.state.key_builder import StorageKey
from maxo.state.manager import StateManager
from maxo.state.storages.base import Storage
from maxo.types.update_context import UpdateContext
from maxo.types.updates.update import Update


class StateManagerMiddleware(Middleware[Update[Any]]):
    def __init__(
        self,
        storage: Storage,
        event_isolation: EventIsolation,
    ) -> None:
        self._storage = storage
        self._event_isolation = event_isolation

    async def execute(
        self,
        ctx: Ctx[Update[Any]],
        update: Update[Any],
        next: NextMiddleware[Update[Any]],
    ) -> Any:
        storage_key = self.make_storage_key(
            bot_id=ctx.bot.state.me.user_id,
            update_context=ctx["update_context"],
        )
        if storage_key is None:
            return await next(ctx)

        state_manager = StateManager(
            key=storage_key,
            storage=self._storage,
        )
        ctx["storage"] = self._storage
        ctx["state_manager"] = state_manager
        ctx["raw_state"] = await state_manager.get_state()

        async with self._event_isolation.lock(key=storage_key):
            return await next(ctx)

    def make_storage_key(
        self,
        bot_id: int,
        update_context: UpdateContext,
    ) -> StorageKey | None:
        chat_id, user_id = update_context.chat_id, update_context.user_id
        if chat_id is None or user_id is None:
            return None

        return StorageKey(
            bot_id=bot_id,
            chat_id=chat_id,
            user_id=user_id,
        )
