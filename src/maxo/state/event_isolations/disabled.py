from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from maxo.state.event_isolations.base import EventIsolation
from maxo.state.key_builder import StorageKey


class DisabledEventIsolation(EventIsolation):
    @asynccontextmanager
    async def lock(self, key: StorageKey) -> AsyncIterator[None]:
        yield

    async def close(self) -> None:
        pass
