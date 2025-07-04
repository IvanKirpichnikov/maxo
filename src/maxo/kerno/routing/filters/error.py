from collections.abc import Callable
from typing import Any, Generic, TypeVar, final

from maxo.kerno.routing.ctx import Ctx
from maxo.kerno.routing.filters.base import Filter
from maxo.kerno.types.updates.error import ErrorEvent

E = TypeVar("E", bound=Exception)


@final
class ErrorFilter(Filter[ErrorEvent[E]], Generic[E]):
    _handler: Callable[[Any], bool]

    __slots__ = ("_handler",)

    def __init__(
        self,
        error: type[E],
        resolve_child: bool = False,
    ) -> None:
        handler = (lambda e: isinstance(e, error)) if resolve_child else lambda e: type(e) is error

        self._handler = handler

    async def execute(
        self,
        update: ErrorEvent[Any],
        ctx: Ctx[ErrorEvent[Any]],
    ) -> bool:
        return self._handler(ctx.update.error)
