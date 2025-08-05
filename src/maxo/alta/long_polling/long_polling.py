import asyncio
import contextlib
from typing import Any, AsyncIterator, Sequence

from maxo import loggers
from maxo.alta.dispatcher import Dispatcher
from maxo.backoff import Backoff, BackoffConfig
from maxo.bot.bot import Bot
from maxo.omit import Omittable, Omitted
from maxo.routing.signals.shutdown import AfterShutdown, BeforeShutdown
from maxo.routing.signals.startup import AfterStartup, BeforeStartup
from maxo.routing.signals.update import Update
from maxo.routing.utils import collect_used_updates

_DEFAULT_BACKOFF_CONFIG = BackoffConfig(
    min_delay=1.0,
    max_delay=5.0,
    factor=1.3,
    jitter=0.1,
)

class LongPolling:
    def __init__(
        self,
        dispatcher: Dispatcher,
        backoff_config: BackoffConfig = _DEFAULT_BACKOFF_CONFIG,
    ) -> None:
        self._dispatcher = dispatcher
        self._backoff_config = backoff_config

        self._lock = asyncio.Lock()

    def run(
        self,
        bot: Bot,
        timeout: Omittable[int] = 30,
        limit: Omittable[int] = 100,
        marker: Omittable[int | None] = Omitted(),
        types: Omittable[Sequence[str]] = Omitted(),
        auto_close_bot: bool = True,
        **workflow_data: Any,
    ) -> None:
        asyncio.run(
            self.start(
                bot=bot,
                timeout=timeout,
                limit=limit,
                marker=marker,
                types=types,
                auto_close_bot=auto_close_bot,
                **workflow_data,
            ),
        )

    async def start(
        self,
        bot: Bot,
        timeout: Omittable[int] = 30,
        limit: Omittable[int] = 100,
        marker: Omittable[int | None] = Omitted(),
        types: Omittable[Sequence[str]] = Omitted(),
        **workflow_data: Any,
    ) -> None:
        dispatcher = self._dispatcher
        dispatcher.workflow_data.update(bot=bot, **workflow_data)

        types = types or collect_used_updates(self._dispatcher)


        async with self._lock:
            await dispatcher.feed_signal(BeforeStartup())
            async with bot:
                loggers.dispatcher.info(
                    "Polling started for @%s id=%s",
                    bot.state.info.username,
                    bot.state.info.user_id,
                )

                await dispatcher.feed_signal(AfterStartup())

                updates_poller = self._get_updates(
                    bot=bot,
                    timeout=timeout,
                    limit=limit,
                    marker=marker,
                    types=types,
                )

                with contextlib.suppress(KeyboardInterrupt):
                    async with asyncio.TaskGroup() as tg:
                        async for update in updates_poller:
                            tg.create_task(dispatcher.feed_max_update(update))

                await dispatcher.feed_signal(BeforeShutdown())

                loggers.dispatcher.info(
                    "Polling stop for @%s bot id=%s",
                    bot.state.info.username,
                    bot.state.info.user_id,
                )

        await dispatcher.feed_signal(AfterShutdown())

    async def _get_updates(
        self,
        bot: Bot,
        timeout: Omittable[int] = 30,
        limit: Omittable[int] = 100,
        marker: Omittable[int | None] = Omitted(),
        types: Omittable[Sequence[str]] = Omitted(),
    ) -> AsyncIterator[Update[Any]]:
        backoff = Backoff(self._backoff_config)
        bot_id = bot.state.info.user_id
        bot_username = bot.state.info.username

        failed = False
        while True:
            try:
                result = await bot.get_updates(
                    limit=limit,
                    timeout=timeout,
                    marker=marker,
                    types=types,
                )
            except Exception as exception:
                failed = True
                loggers.dispatcher.error(
                    "Failed to fetch updates - %s: %s",
                    type(exception).__name__,
                    exception,
                )
                loggers.dispatcher.warning(
                    "Sleep for %f seconds and try again... (tryings = %d, username = @%s, bot id = %d)",
                    backoff.current_delay,
                    backoff.counter,
                    bot_username,
                    bot_id,
                )
                backoff.next()
                continue

            if failed:
                loggers.dispatcher.info(
                    "Connection established (tryings = %d, username = @%s, bot id = %d)",
                    backoff.counter,
                    bot_username,
                    bot_id,
                )
                backoff.reset()
                failed = False

            for update in result.updates:
                yield Update(
                    update=update,
                    marker=result.marker
                )

            marker = result.marker
