from collections import deque
from collections.abc import AsyncIterator, Iterable
from typing import cast, overload

from typing_extensions import Self

from maxo.kerno.bot.bot import Bot
from maxo.kerno.types.types.chat_member import ChatMember
from maxo.omit import Omittable, Omitted


class ChatMembersIterator(AsyncIterator[ChatMember]):
    _marker: Omittable[int | None]
    _chat_members: deque[ChatMember]

    __slots__ = (
        "_bot",
        "_chat_id",
        "_chat_members",
        "_count",
        "_marker",
        "_user_ids",
    )

    @overload
    def __init__(
        self,
        bot: Bot,
        chat_id: int,
        user_ids: Iterable[int],
        marker: Omittable[int] = Omitted(),
        count: Omittable[int] = Omitted(),
    ) -> None: ...

    @overload
    def __init__(
        self,
        bot: Bot,
        chat_id: int,
        user_ids: Omittable[None] = Omitted(),
        marker: Omittable[int] = Omitted(),
        count: Omittable[int] = 20,
    ) -> None: ...

    def __init__(
        self,
        bot: Bot,
        chat_id: int,
        user_ids: Omittable[Iterable[int] | None] = Omitted(),
        marker: Omittable[int] = Omitted(),
        count: Omittable[int] = 20,
    ) -> None:
        self._bot = bot
        self._chat_id = chat_id

        self._user_ids = user_ids
        self._marker = marker
        self._count = count

        self._chat_members = deque()

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> ChatMember:
        if self._chat_members:
            return self._chat_members.popleft()

        while True:
            result = await self._bot.get_chat_members(
                chat_id=self._chat_id,
                user_ids=self._user_ids,
                marker=cast("int | Omitted", self._marker),
                count=self._count,
            )
            self._marker = result.marker

            if not result.members:
                raise StopAsyncIteration

            self._chat_members.extend(result.members)

            return self._chat_members.popleft()
