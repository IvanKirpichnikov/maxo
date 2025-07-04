from collections.abc import MutableMapping
from typing import Any

from maxo.alta.state.key_builder import StorageKey
from maxo.alta.state.state import State
from maxo.alta.state.storages.base import Storage


class StateManager:
    __slots__ = ("key", "storage")

    def __init__(self, storage: Storage, key: StorageKey) -> None:
        self.key = key
        self.storage = storage

    async def set_state(self, state: State | None = None) -> None:
        await self.storage.set_state(key=self.key, state=state)

    async def get_raw_data(self) -> str | None:
        return await self.storage.get_raw_data(key=self.key)

    async def set_data(self, data: MutableMapping[str, Any]) -> None:
        await self.storage.set_data(key=self.key, data=data)

    async def get_data(self) -> MutableMapping[str, Any]:
        return await self.storage.get_data(key=self.key)

    async def get_value(self, key: str, default: Any | None = None) -> Any | None:
        return await self.storage.get_value(storage_key=self.key, value_key=key, default=default)

    async def update_data(
        self, data: MutableMapping[str, Any] | None = None, **kwargs: Any
    ) -> MutableMapping[str, Any]:
        if data:
            kwargs.update(data)
        return await self.storage.update_data(key=self.key, data=kwargs)

    async def clear(self) -> None:
        await self.set_state(state=None)
        await self.set_data({})
