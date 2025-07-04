from abc import abstractmethod
from typing import Any, Protocol, TypeVar

from maxo.kerno.routing.ctx import Ctx
from maxo.kerno.types.updates.base import BaseUpdate

U = TypeVar("U", bound=BaseUpdate)


class NextMiddleware(Protocol[U]):
    __slots__ = ()

    @abstractmethod
    async def __call__(self, ctx: Ctx[U]) -> Any:
        raise NotImplementedError


class Middleware(Protocol[U]):
    __slots__ = ()

    @abstractmethod
    async def execute(
        self,
        update: U,
        ctx: Ctx[U],
        next: NextMiddleware[U],
    ) -> Any:
        raise NotImplementedError
