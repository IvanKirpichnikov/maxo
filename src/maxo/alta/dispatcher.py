import asyncio
from collections.abc import MutableMapping
from typing import Any

from maxo import loggers
from maxo.alta.facades.middleware import FacadeMiddleware
from maxo.alta.state_system.event_isolations.base import EventIsolation
from maxo.alta.state_system.event_isolations.simple import SimpleEventIsolation
from maxo.alta.state_system.middleware import StateManagerMiddleware
from maxo.alta.state_system.storages.base import Storage
from maxo.alta.state_system.storages.memory import MemoryStorage
from maxo.routing.ctx import Ctx
from maxo.routing.middlewares.error import ErrorMiddleware
from maxo.routing.middlewares.update_context import UpdateContextMiddleware
from maxo.routing.observers.signal import SignalObserver
from maxo.routing.routers.simple import SimpleRouter
from maxo.routing.sentinels import UNHANDLED
from maxo.routing.signals.base import BaseSignal
from maxo.routing.signals.startup import BeforeStartup
from maxo.routing.signals.update import Update
from maxo.routing.updates.base import BaseUpdate
from maxo.routing.utils._resolving_inner_middlewares import resolving_inner_middlewares
from maxo.routing.utils.validate_router_graph import validate_router_graph


class Dispatcher(SimpleRouter):
    update: SignalObserver[Update[Any]]

    def __init__(
        self,
        *,
        workflow_data: MutableMapping[str, Any] | None = None,
        # State system settings
        storage: Storage | None = None,
        event_isolation: EventIsolation | None = None,
    ) -> None:
        super().__init__(self.__class__.__name__)

        self.workflow_data = workflow_data or {}
        self.workflow_data["dispatcher"] = self

        self.update = self._observers[Update] = SignalObserver()
        self.update.middleware.outer(ErrorMiddleware(self))
        self.update.middleware.outer(UpdateContextMiddleware())

        self.update.handler(self._feed_update_handler)

        # State system settings
        if storage is None:
            storage = MemoryStorage()

        if event_isolation is None:
            event_isolation = SimpleEventIsolation()

        self.update.middleware.outer(StateManagerMiddleware(storage, event_isolation))

        # Facade settings

        self.update.middleware.outer(FacadeMiddleware())


    async def feed_max_update(self, update: Update[Any]) -> Any:
        loop = asyncio.get_running_loop()
        start_time = loop.time()

        result = UNHANDLED

        try:
            result = await self.feed_update(update)
        except Exception:
            duration = (loop.time() - start_time) * 1000
            loggers.dispatcher.exception(
                "%s update failed. Update type=%r marker=%r. Duration %d ms",
                "Handled" if result is not UNHANDLED else "Not handled",
                update.update.__class__.__name__,
                update.marker,
                duration,
            )
        else:
            duration = (loop.time() - start_time) * 1000
            loggers.dispatcher.info(
                "%s update completed %r. Update type=%r marker=%r. Duration %d ms",
                "Handled" if result is not UNHANDLED else "Not handled",
                result,
                update.update.__class__.__name__,
                update.marker,
                duration,
            )
        return result

    async def feed_signal(self, signal: BaseSignal) -> Any:
        return await self.feed_update(signal)

    async def feed_update(self, update: BaseUpdate) -> Any:
        ctx = Ctx.factory(update, self.workflow_data)
        return await self.trigger(ctx)

    async def _feed_update_handler(
        self,
        ctx: Ctx[Update[Any]],
    ) -> Any:
        ctx = Ctx.factory(ctx.update.update, ctx._state._data)
        return await self.trigger(ctx)

    async def _emit_before_startup_handler(self, ctx: Ctx[BeforeStartup]) -> None:
        validate_router_graph(self)
        resolving_inner_middlewares(self)

        await super()._emit_before_startup_handler(ctx)
