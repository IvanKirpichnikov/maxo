import asyncio
import contextlib
from collections.abc import Iterable, MutableMapping
from copy import copy
from typing import Any

from anyio import Lock, create_task_group

from maxo import loggers
from maxo.alta.state.event_isolations.base import EventIsolation
from maxo.alta.state.event_isolations.simple import SimpleEventIsolation
from maxo.alta.state.storages.base import Storage
from maxo.alta.state.storages.memory import MemoryStorage
from maxo.bot.bot import Bot
from maxo.omit import Omittable, Omitted
from maxo.routing.dispatcher.ctx import Ctx
from maxo.routing.dispatcher.long_polling import LongPolling
from maxo.routing.dispatcher.observer import UpdateObserver
from maxo.routing.dispatcher.router import Router, RouterProtocol
from maxo.routing.dispatcher.sentinels import UNHANDLED
from maxo.routing.middlewares.error import ErrorMiddleware
from maxo.routing.middlewares.facade import FacadeMiddleware
from maxo.routing.middlewares.state_manager import StateManagerMiddleware
from maxo.routing.middlewares.update_context import UpdateContextMiddleware
from maxo.types.updates.shutdown import Shutdown
from maxo.types.updates.startup import Startup
from maxo.types.updates.update import Update


class Dispatcher(Router):
    update: UpdateObserver[Update[Any]]
    workflow_data: MutableMapping[str, Any]

    _lock: Lock

    def __init__(
        self,
        storage: Storage | None = None,
        event_isolation: EventIsolation | None = None,
        workflow_data: MutableMapping[str, Any] | None = None,
    ) -> None:
        super().__init__(self.__class__.__name__)

        if storage is None:
            storage = MemoryStorage()

        if event_isolation is None:
            event_isolation = SimpleEventIsolation()

        self.workflow_data = workflow_data or {}
        self.workflow_data["dispatcher"] = self

        self.update = self.observers[Update] = UpdateObserver()

        self.update.outer_middleware(ErrorMiddleware(self))
        self.update.outer_middleware(UpdateContextMiddleware())
        self.update.outer_middleware(StateManagerMiddleware(storage, event_isolation))
        self.update.outer_middleware(FacadeMiddleware())

        self.update.add_handler(self._feed_update_handler)

        self._lock = Lock()

    @property
    def parent_router(self) -> RouterProtocol | None:
        raise RuntimeError("This is the parent router")

    async def _feed_update_handler(
        self,
        update: Update[Any],
        /,
        **kwargs: Any,
    ) -> None:
        ctx = Ctx(update.update, kwargs)
        await self.trigger(ctx)

    async def feed_update(
        self,
        update: Update[Any],
    ) -> None:
        ctx = Ctx(update, copy(self.workflow_data))

        loop = asyncio.get_running_loop()
        start_time = loop.time()

        result = UNHANDLED

        try:
            result = await self.trigger(ctx)
        except Exception:
            duration = (loop.time() - start_time) * 1000
            loggers.dispathing.exception(
                "%s update failed. Update type=%r marker=%r. Duration %d ms",
                "Handled" if result is not UNHANDLED else "Not handled",
                update.update.__class__.__name__,
                update.marker,
                duration,
            )
        else:
            duration = (loop.time() - start_time) * 1000
            loggers.dispathing.info(
                "%s update completed %r. Update type=%r marker=%r. Duration %d ms",
                "Handled" if result is not UNHANDLED else "Not handled",
                result,
                update.update.__class__.__name__,
                update.marker,
                duration,
            )

    async def start_polling(
        self,
        bot: Bot,
        timeout: Omittable[int] = 30,
        limit: Omittable[int] = 100,
        marker: Omittable[int | None] = Omitted(),
        types: Omittable[Iterable[str]] = Omitted(),
        **workflow_data: Any,
    ) -> None:
        self.workflow_data.update(bot=bot, **workflow_data)

        updates_poller = LongPolling(
            bot=bot,
            limit=limit,
            timeout=timeout,
            marker=marker,
            types=types,
        )
        async with self._lock, bot:
            loggers.dispathing.info("Polling started")
            await self.trigger(Ctx(Startup(), copy(self.workflow_data)))

            with contextlib.suppress(KeyboardInterrupt):
                async with create_task_group() as tg:
                    async for update in updates_poller:
                        tg.start_soon(self.feed_update, update)

            loggers.dispathing.info("Polling stopped")
            await self.trigger(Ctx(Shutdown(), copy(self.workflow_data)))

    def run_polling(
        self,
        bot: Bot,
        timeout: Omittable[int] = 30,
        limit: Omittable[int] = 100,
        marker: Omittable[int | None] = Omitted(),
        types: Omittable[Iterable[str]] = Omitted(),
        auto_close_bot: bool = True,
        **workflow_data: Any,
    ) -> None:
        asyncio.run(
            self.start_polling(
                bot=bot,
                timeout=timeout,
                limit=limit,
                marker=marker,
                types=types,
                auto_close_bot=auto_close_bot,
                **workflow_data,
            ),
        )
