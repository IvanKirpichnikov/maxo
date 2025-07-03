from collections import deque
from collections.abc import AsyncIterator, Iterable
from logging import getLogger
from typing import Any

from retejo.markers import Omittable
from typing_extensions import Self

from maxo.bot.bot import Bot
from maxo.types.updates import Updates
from maxo.types.updates.update import Update

logger = getLogger(__name__)


class LongPolling(AsyncIterator[Update[Any]]):
    def __init__(
        self,
        bot: Bot,
        limit: Omittable[int],
        timeout: Omittable[int],
        marker: Omittable[int | None],
        types: Omittable[Iterable[str]],
    ) -> None:
        self._bot = bot
        self._marker = marker
        self._limit = limit
        self._timeout = timeout
        self._types = types

        self._updates: deque[Updates] = deque()

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> Update[Any]:
        if self._updates:
            return self._pop_update()

        while True:
            result = await self._bot.get_updates(
                limit=self._limit,
                timeout=self._timeout,
                marker=self._marker,
                types=self._types,
            )

            if not result.updates:
                continue

            self._updates.extend(result.updates)
            self._marker = result.marker

            return self._pop_update()

    def _pop_update(self) -> Update[Any]:
        update = self._updates.popleft()
        marker = self._marker if isinstance(self._marker, int) else None

        return Update(
            update=update,
            marker=marker,
        )
