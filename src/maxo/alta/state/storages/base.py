from abc import abstractmethod
from collections.abc import MutableMapping
from copy import copy
from typing import Any, Protocol

from maxo.alta.state.key_builder import StorageKey
from maxo.alta.state.state import State


class Storage(Protocol):
    @abstractmethod
    async def set_state(
        self,
        key: StorageKey,
        state: State | None = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_state(self, key: StorageKey) -> str | None:
        raise NotImplementedError

    @abstractmethod
    async def set_data(
        self,
        key: StorageKey,
        data: MutableMapping[str, Any],
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_data(self, key: StorageKey) -> MutableMapping[str, Any]:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError

    async def get_value(self, storage_key: StorageKey, value_key: str, default: Any | None = None) -> Any | None:
        data = await self.get_data(storage_key)
        return copy(data.get(value_key, default))

    async def update_data(
        self,
        key: StorageKey,
        data: MutableMapping[str, Any],
    ) -> MutableMapping[str, Any]:
        current_data = await self.get_data(key=key)
        current_data.update(data)
        await self.set_data(key=key, data=current_data)

        return copy(current_data)
