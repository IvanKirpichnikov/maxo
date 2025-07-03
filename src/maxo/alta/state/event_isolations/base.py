from abc import abstractmethod
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Protocol

from maxo.alta.state.key_builder import StorageKey


class EventIsolation(Protocol):
    @abstractmethod
    @asynccontextmanager
    async def lock(self, key: StorageKey) -> AsyncIterator[None]:
        yield None

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError
