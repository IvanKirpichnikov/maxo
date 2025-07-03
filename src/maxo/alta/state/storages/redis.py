import json
from collections.abc import Callable, MutableMapping
from typing import Any, cast

from redis.asyncio import Redis
from redis.typing import ExpiryT

from maxo.alta.state.key_builder import DefaultKeyBuilder, KeyBuilder, StorageKey, StorageKeyType
from maxo.alta.state.state import State
from maxo.alta.state.storages.base import Storage


class RedisStorage(Storage):
    def __init__(
        self,
        redis: Redis,
        key_builder: KeyBuilder | None = None,
        state_ttl: ExpiryT | None = None,
        data_ttl: ExpiryT | None = None,
        json_loads: Callable[[Any], Any] = json.loads,
        json_dumps: Callable[[Any], str] = json.dumps,
    ) -> None:
        if key_builder is None:
            key_builder = DefaultKeyBuilder()

        self.redis = redis
        self.key_builder = key_builder
        self.state_ttl = state_ttl
        self.data_ttl = data_ttl
        self.json_loads = json_loads
        self.json_dumps = json_dumps

    async def set_state(
        self,
        key: StorageKey,
        state: State | None = None,
    ) -> None:
        built_key = self.key_builder.build(key, StorageKeyType.STATE)
        if state is None:
            await self.redis.delete(built_key)
        else:
            await self.redis.set(
                built_key,
                state.state,
                ex=self.state_ttl,
            )

    async def get_state(
        self,
        key: StorageKey,
    ) -> str | None:
        built_key = self.key_builder.build(key, StorageKeyType.STATE)
        value = await self.redis.get(built_key)
        if isinstance(value, bytes):
            return value.decode("utf-8")
        return cast("str | None", value)

    async def set_data(
        self,
        key: StorageKey,
        data: MutableMapping[str, Any],
    ) -> None:
        built_key = self.key_builder.build(key, StorageKeyType.DATA)
        if not data:
            await self.redis.delete(built_key)
        else:
            await self.redis.set(
                built_key,
                self.json_dumps(data),
                ex=self.data_ttl,
            )

    async def get_data(
        self,
        key: StorageKey,
    ) -> MutableMapping[str, Any]:
        built_key = self.key_builder.build(key, StorageKeyType.DATA)
        value = await self.redis.get(built_key)
        if value is None:
            return {}

        if isinstance(value, bytes):
            value = value.decode("utf-8")

        return cast("MutableMapping[str, Any]", self.json_loads(value))

    async def close(self) -> None:
        await self.redis.aclose()
