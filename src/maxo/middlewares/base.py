from abc import abstractmethod
from typing import Any, Protocol, TypeVar

from maxo.dispatcher.ctx import Ctx
from maxo.types.updates.base import BaseUpdate

U = TypeVar("U", bound=BaseUpdate)


class NextMiddleware(Protocol[U]):
    @abstractmethod
    async def __call__(self, ctx: Ctx[U]) -> Any:
        raise NotImplementedError


class Middleware(Protocol[U]):
    @abstractmethod
    async def execute(
        self,
        update: U,
        ctx: Ctx[U],
        next: NextMiddleware[U],
    ) -> Any:
        raise NotImplementedError
