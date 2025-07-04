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
from maxo.kerno.bot.bot import Bot
from maxo.kerno.routing.ctx import Ctx
from maxo.kerno.routing.executors.long_polling import LongPolling
from maxo.kerno.routing.middlewares.error import ErrorMiddleware
from maxo.kerno.routing.middlewares.facade import FacadeMiddleware
from maxo.kerno.routing.middlewares.state_manager import StateManagerMiddleware
from maxo.kerno.routing.middlewares.update_context import UpdateContextMiddleware
from maxo.kerno.routing.routing.observer import UpdateObserver
from maxo.kerno.routing.routing.router import Router, RouterProtocol
from maxo.kerno.routing.routing.walking_graph import walking_router_graph
from maxo.kerno.routing.sentinels import UNHANDLED
from maxo.kerno.types.updates.shutdown import Shutdown
from maxo.kerno.types.updates.startup import Startup
from maxo.kerno.types.updates.update import Update
from maxo.omit import Omittable, Omitted


class Dispatcher(Router):
    update: UpdateObserver[Update[Any]]
    workflow_data: MutableMapping[str, Any]

    _lock: Lock

    __slots__ = (
        "_lock",
        "update",
        "workflow_data",
    )

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
            loggers.dispatching.exception(
                "%s update failed. Update type=%r marker=%r. Duration %d ms",
                "Handled" if result is not UNHANDLED else "Not handled",
                update.update.__class__.__name__,
                update.marker,
                duration,
            )
        else:
            duration = (loop.time() - start_time) * 1000
            loggers.dispatching.info(
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
            types=walking_router_graph(self),
        )
        async with self._lock, bot:
            loggers.dispatching.info("Polling started")
            await self.trigger(Ctx(Startup(), copy(self.workflow_data)))

            with contextlib.suppress(KeyboardInterrupt):
                async with create_task_group() as tg:
                    async for update in updates_poller:
                        tg.start_soon(self.feed_update, update)

            loggers.dispatching.info("Polling stopped")
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
