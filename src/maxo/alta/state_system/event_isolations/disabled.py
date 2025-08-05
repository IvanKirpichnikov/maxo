from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from maxo.alta.state_system.event_isolations.base import EventIsolation
from maxo.alta.state_system.key_builder import StorageKey


class DisabledEventIsolation(EventIsolation):
    @asynccontextmanager
    async def lock(self, key: StorageKey) -> AsyncIterator[None]:
        yield

    async def close(self) -> None:
        pass
