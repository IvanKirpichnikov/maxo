import asyncio
from collections.abc import Iterable, MutableMapping
from copy import copy
from logging import getLogger
from typing import Any

from anyio import Lock, create_task_group

from maxo.bot.bot import Bot
from maxo.dispatcher.ctx import Ctx
from maxo.dispatcher.long_polling import LongPolling
from maxo.dispatcher.observer import UpdateObserver
from maxo.dispatcher.router import Router
from maxo.dispatcher.sentinels import UNHANDLED
from maxo.middlewares.error import ErrorMiddleware
from maxo.middlewares.facade import FacadeMiddleware
from maxo.middlewares.state_manager import StateManagerMiddleware
from maxo.middlewares.update_context import UpdateContextMiddleware
from maxo.omit import Omittable, Omitted
from maxo.state.event_isolations.base import EventIsolation
from maxo.state.event_isolations.simple import SimpleEventIsolation
from maxo.state.storages.base import Storage
from maxo.state.storages.memory import MemoryStorage
from maxo.types.updates.shutdown import Shutdown
from maxo.types.updates.startup import Startup
from maxo.types.updates.update import Update

logger = getLogger(__name__)


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
            logger.exception(
                "%s update failed. Update type=%r marker=%r. Duration %d ms",
                "Handled" if result is not UNHANDLED else "Not handled",
                update.update.__class__.__name__,
                update.marker,
                duration,
            )
        else:
            duration = (loop.time() - start_time) * 1000
            logger.info(
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
        auto_close_bot: bool = True,
        **workflow_data: Any,
    ) -> None:
        await bot.start()

        self.workflow_data.update(bot=bot, **workflow_data)

        updates_poller = LongPolling(
            bot=bot,
            limit=limit,
            timeout=timeout,
            marker=marker,
            types=types,
        )
        async with self._lock:
            logger.info("Polling started")
            await self.trigger(Ctx(Startup(), copy(self.workflow_data)))
            try:
                async with create_task_group() as tg:
                    async for update in updates_poller:
                        tg.start_soon(self.feed_update, update)
            except KeyboardInterrupt:
                pass
            finally:
                logger.info("Polling stopped")
                await self.trigger(Ctx(Shutdown(), copy(self.workflow_data)))
                if auto_close_bot:
                    await bot.close()

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
