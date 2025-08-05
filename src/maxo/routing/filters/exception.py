from collections.abc import Callable
from typing import Any, Generic, TypeVar, final

from maxo.routing.ctx import Ctx
from maxo.routing.filters.base import BaseFilter
from maxo.routing.signals.exception import ExceptionEvent

_ExceptionT = TypeVar("_ExceptionT", bound=Exception)


@final
class ExceptionFilter(BaseFilter[ExceptionEvent[_ExceptionT]], Generic[_ExceptionT]):
    _handler: Callable[[Any], bool]

    __slots__ = ("_handler",)

    def __init__(
        self,
        error: type[_ExceptionT],
        use_subclass: bool = False,
    ) -> None:
        if use_subclass:
            self._handler = lambda e: isinstance(e, error)
        else:
            self._handler = lambda e: type(e) is error

    async def execute(
        self,
        update: ExceptionEvent[Any],
        ctx: Ctx[ExceptionEvent[Any]],
    ) -> bool:
        return self._handler(update.error)
