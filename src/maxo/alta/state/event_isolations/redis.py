from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from redis.asyncio import Redis
from redis.asyncio.lock import Lock

from maxo.alta.state.event_isolations.base import EventIsolation
from maxo.alta.state.key_builder import DefaultKeyBuilder, KeyBuilder, StorageKey, StorageKeyType

DEFAULT_REDIS_LOCK_KWARGS = {"timeout": 60}


class RedisEventIsolation(EventIsolation):
    def __init__(
        self,
        redis: Redis,
        key_builder: KeyBuilder | None = None,
        lock_kwargs: dict[str, Any] | None = None,
    ) -> None:
        if key_builder is None:
            key_builder = DefaultKeyBuilder()
        if lock_kwargs is None:
            lock_kwargs = DEFAULT_REDIS_LOCK_KWARGS

        self.redis = redis
        self.key_builder = key_builder
        self.lock_kwargs = lock_kwargs

    @asynccontextmanager
    async def lock(
        self,
        key: StorageKey,
    ) -> AsyncIterator[None]:
        redis_key = self.key_builder.build(key, StorageKeyType.LOCK)
        async with self.redis.lock(name=redis_key, **self.lock_kwargs, lock_class=Lock):
            yield

    async def close(self) -> None:
        await self.redis.aclose()
