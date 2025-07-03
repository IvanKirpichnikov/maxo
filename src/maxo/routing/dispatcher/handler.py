import inspect
from collections.abc import Callable, Coroutine, Mapping
from inspect import Parameter, Signature, _empty
from typing import (
    Any,
    Concatenate,
    Generic,
    ParamSpec,
    TypeAlias,
    TypeVar,
)

from maxo.routing.dispatcher.ctx import Ctx
from maxo.routing.filters.base import Filter
from maxo.types.updates.base import BaseUpdate

T = TypeVar("T")
P = ParamSpec("P")
U = TypeVar("U", bound=BaseUpdate)

HandlerFn: TypeAlias = Callable[Concatenate[U, P], Coroutine[Any, Any, T]]
_DataGetter: TypeAlias = Callable[[Mapping[str, Any]], Mapping[str, Any]]


def _kwargs_only_data_getter(
    data: Mapping[str, Any],
) -> Mapping[str, Any]:
    return data


def _data_getter_by_signature(
    signature: Signature,
) -> _DataGetter:
    def wrapper(
        data: Mapping[str, Any],
    ) -> Mapping[str, Any]:
        kwargs: dict[str, Any] = {}

        for param in list(signature.parameters.values())[1:]:
            if param.default is not _empty:
                kwargs[param.name] = data.get(param.name, param.default)
            else:
                kwargs[param.name] = data[param.name]
        return kwargs

    return wrapper


class Handler(Generic[U, P, T]):
    _data_getter: _DataGetter

    def __init__(
        self,
        handler_fn: HandlerFn[U, P, T],
        filter: Filter[U] | None = None,
    ) -> None:
        self._filter = filter
        self._handler_fn = handler_fn

        signature = inspect.signature(handler_fn)
        for param in signature.parameters.values():
            if param.kind is Parameter.VAR_KEYWORD:
                self._data_getter = _kwargs_only_data_getter
                break
        else:
            self._data_getter = _data_getter_by_signature(signature)

    def __repr__(self) -> str:
        return f"Handler(func={self._handler_fn}, filter={self._filter})"

    async def execute_filter(self, ctx: Ctx[U]) -> bool:
        if self._filter is None:
            return True

        return await self._filter.execute(ctx.update, ctx)

    async def execute(self, ctx: Ctx[U]) -> T:
        kwargs = self._data_getter(ctx.data)
        return await self._handler_fn(ctx.update, **kwargs)  # type: ignore[call-arg]
