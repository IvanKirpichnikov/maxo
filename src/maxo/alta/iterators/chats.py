from collections import deque
from collections.abc import AsyncIterator

from typing_extensions import Self

from maxo.kerno.bot.bot import Bot
from maxo.kerno.types.types.chat import Chat
from maxo.omit import Omittable, is_omitted


class ChatsIterator(AsyncIterator[Chat]):
    __slots__ = (
        "_bot",
        "_chats",
        "_count",
        "_marker",
    )

    def __init__(
        self,
        bot: Bot,
        count: Omittable[int] = 50,
        marker: Omittable[int | None] = None,
    ) -> None:
        self._bot = bot
        self._count = count
        self._marker = marker

        self._chats: deque[Chat] = deque()

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> Chat:
        if self._chats:
            return self._chats.popleft()

        while True:
            result = await self._bot.get_chats(
                count=self._count,
                marker=self._marker,
            )

            if result.marker is None or is_omitted(result.marker):
                raise StopAsyncIteration

            self._chats.extend(result.chats)
            self._marker = result.marker

            return self._chats.popleft()
