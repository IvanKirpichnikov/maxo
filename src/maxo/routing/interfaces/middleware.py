from abc import abstractmethod
from typing import Any, Protocol, TypeVar, runtime_checkable

from maxo.routing.ctx import Ctx
from maxo.routing.updates.base import BaseUpdate

_UpdateT = TypeVar("_UpdateT", bound=BaseUpdate)


@runtime_checkable
class NextMiddleware(Protocol[_UpdateT]):
    __slots__ = ()

    @abstractmethod
    async def __call__(self, ctx: Ctx[_UpdateT]) -> Any:
        raise NotImplementedError


@runtime_checkable
class Middleware(Protocol[_UpdateT]):
    __slots__ = ()

    @abstractmethod
    async def execute(
        self,
        update: _UpdateT,
        ctx: Ctx[_UpdateT],
        next: NextMiddleware[_UpdateT],
    ) -> Any:
        raise NotImplementedError
