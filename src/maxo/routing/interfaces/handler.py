from abc import abstractmethod
from typing import (
    Protocol,
    TypeVar,
)

from maxo.routing.ctx import Ctx
from maxo.routing.updates.base import BaseUpdate

_UpdateT = TypeVar("_UpdateT", bound=BaseUpdate)
_ReturnT_co = TypeVar("_ReturnT_co", covariant=True)


class Handler(Protocol[_UpdateT, _ReturnT_co]):
    __slots__ = ()

    @abstractmethod
    async def execute_filter(self, ctx: Ctx[_UpdateT]) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def execute(self, ctx: Ctx[_UpdateT]) -> _ReturnT_co:
        raise NotImplementedError
