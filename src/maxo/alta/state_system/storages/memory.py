from collections.abc import MutableMapping
from copy import copy
from typing import Any

from maxo.alta.state_system.key_builder import (
    DefaultKeyBuilder,
    KeyBuilder,
    StorageKey,
    StorageKeyType,
)
from maxo.alta.state_system.state import State
from maxo.alta.state_system.storages.base import Storage


class MemoryStorage(Storage):
    _state: MutableMapping[str, str | None]
    _data: MutableMapping[str, MutableMapping[str, Any]]

    __slots__ = ("_data", "_key_builder", "_state")

    def __init__(
        self,
        key_builder: KeyBuilder | None = None,
    ) -> None:
        self._data = {}
        self._state = {}

        if key_builder is None:
            key_builder = DefaultKeyBuilder()
        self._key_builder = key_builder

    async def set_state(self, key: StorageKey, state: State | None = None) -> None:
        built_key = self._key_builder.build(key, StorageKeyType.STATE)

        if state is None:
            self._state[built_key] = None
        else:
            self._state[built_key] = state.state

    async def get_state(self, key: StorageKey) -> str | None:
        built_key = self._key_builder.build(key, StorageKeyType.STATE)
        return self._state.get(built_key)

    async def set_data(self, key: StorageKey, data: MutableMapping[str, Any]) -> None:
        built_key = self._key_builder.build(key, StorageKeyType.DATA)
        self._data[built_key] = copy(data)

    async def get_data(self, key: StorageKey) -> MutableMapping[str, Any]:
        built_key = self._key_builder.build(key, StorageKeyType.DATA)
        return copy(self._data.get(built_key, {}))

    async def close(self) -> None:
        self._data.clear()
        self._state.clear()
