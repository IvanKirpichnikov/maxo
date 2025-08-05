from abc import abstractmethod
from collections.abc import Callable
from typing import Any, Coroutine, Protocol, Sequence, TypeVar

from maxo.routing.ctx import Ctx
from maxo.routing.interfaces.filter import Filter
from maxo.routing.interfaces.handler import Handler
from maxo.routing.middlewares.manager import MiddlewareManagerFacade
from maxo.routing.updates.base import BaseUpdate

_UpdateT = TypeVar("_UpdateT", bound=BaseUpdate)
_ReturnT_co = TypeVar("_ReturnT_co", covariant=True)

_HandlerT = TypeVar("_HandlerT", bound=Handler[Any, Any])
_HandlerFnT = TypeVar("_HandlerFnT", bound=Callable[..., Coroutine[Any, Any, Any]])

class ObserverState(Protocol):
    @abstractmethod
    def ensure_add_handler(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def ensure_add_filter(self) -> None:
        raise NotImplementedError


class Observer(Protocol[_UpdateT, _HandlerT, _HandlerFnT]):
    @property
    @abstractmethod
    def _state(self) -> ObserverState:
        raise NotImplementedError

    @_state.setter
    @abstractmethod
    def _state(self, value: ObserverState) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def handlers(self) -> Sequence[_HandlerT]:
        raise NotImplementedError

    @property
    @abstractmethod
    def middleware(self) -> MiddlewareManagerFacade[_UpdateT]:
        raise NotImplementedError

    @abstractmethod
    def __call__(
        self,
        filter: Filter[_UpdateT] | None = None,
    ) -> Callable[[_HandlerFnT], _HandlerFnT]:
        raise NotImplementedError

    @abstractmethod
    def handler(
        self,
        handler_fn: _HandlerFnT,
        filter: Filter[_UpdateT] | None = None,
    ) -> _HandlerFnT:
        raise NotImplementedError

    @abstractmethod
    def filter(self, filter: Filter[_UpdateT]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def execute_filter(self, ctx: Ctx[_UpdateT]) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def handler_lookup(self, ctx: Ctx[_UpdateT]) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def execute_handler(
        self,
        ctx: Ctx[_UpdateT],
        handler: _HandlerT,
    ) -> _ReturnT_co:
        raise NotImplementedError
