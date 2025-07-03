from asyncio import Lock
from collections import defaultdict
from collections.abc import AsyncIterator, Hashable
from contextlib import asynccontextmanager

from maxo.alta.state.event_isolations.base import EventIsolation
from maxo.alta.state.key_builder import DefaultKeyBuilder, KeyBuilder, StorageKey, StorageKeyType


class SimpleEventIsolation(EventIsolation):
    def __init__(
        self,
        key_builder: KeyBuilder | None = None,
    ) -> None:
        if key_builder is None:
            key_builder = DefaultKeyBuilder()
        self._key_builder = key_builder

        self._locks: defaultdict[Hashable, Lock] = defaultdict(Lock)

    @asynccontextmanager
    async def lock(self, key: StorageKey) -> AsyncIterator[None]:
        built_key = self._key_builder.build(key, StorageKeyType.LOCK)

        lock = self._locks[built_key]
        async with lock:
            yield

    async def close(self) -> None:
        self._locks.clear()
