from collections.abc import MutableMapping
from copy import copy
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from typing_extensions import (
    Generic as GenericExtensions,
    TypeVar as TypeVarExtensions,
)

from maxo.omit import Omitted
from maxo.routing.updates.base import BaseUpdate
from maxo.types.maybe import Maybe

_UpdateT = TypeVar("_UpdateT", bound=BaseUpdate)
_CtxDataT = TypeVarExtensions("_CtxDataT", default=Any)

_sentinel = Omitted()

class CtxState:
    __slots__ = ("_data",)

    _data: dict[str, Any]

    def __init__(
        self,
        initial_data: MutableMapping[str, Any] | None = None,
    ) -> None:
        object.__setattr__(self, "_data", dict(initial_data) if initial_data else {})

    @property
    def raw_data(self) -> MutableMapping[str, Any]:
        return self._data.copy()

    def copy(self) -> "CtxState":
        return CtxState(copy(self._data))

    def __setattr__(self, name: str, value: Any) -> None:
        self._data[name] = value

    def __getattr__(self, name: str) -> Any:
        result = self._data.get(name, _sentinel)
        if result is _sentinel:
            raise AttributeError(f"Attribute {name!r} not found", name=name)

        return result


class Ctx(GenericExtensions[_UpdateT, _CtxDataT]):
    _update: _UpdateT
    _state: CtxState

    __slots__ = ("_state", "_update")

    def __init__(
        self,
        update: _UpdateT,
        state: CtxState,
    ) -> None:
        state.update = update
        state.state = state
        state.update_tp = type(update)

        object.__setattr__(self, "_update", update)
        object.__setattr__(self, "_state", state)

    @property
    def data(self) -> _CtxDataT:
        return cast("_CtxDataT", self._state)

    @property
    def state(self) -> CtxState:
        return self._state

    @property
    def raw_data(self) -> MutableMapping[str, Any]:
        return self._state.raw_data

    @classmethod
    def factory(
        cls,
        update: _UpdateT,
        initial_data: MutableMapping[str, Any] | None = None,
    ) -> "Ctx[_UpdateT]":
        state = CtxState(copy(initial_data) if initial_data is not None else None)
        return cls(update, state)

    def copy(self) -> "Ctx[_UpdateT, _CtxDataT]":
        return Ctx(self._update, self._state.copy())

    def merge(self, other: "Ctx[_UpdateT, _CtxDataT]") -> Self:
        self._state._data = {**other._state._data, **self._state._data}
        return self

    def __getattr__(self, name: str) -> Any:
        return getattr(self._state, name)

    def __setattr__(self, name: str, value: Any) -> Any:
        setattr(self._state, name, value)

    if TYPE_CHECKING:
        from maxo.alta.dispatcher import Dispatcher
        from maxo.alta.facades.updates.base import BaseUpdateFacade
        from maxo.alta.state_system.manager import StateManager
        from maxo.alta.state_system.storages.base import Storage
        from maxo.bot.bot import Bot
        from maxo.types.update_context import UpdateContext

        update: _UpdateT
        update_tp: type[_UpdateT]
        update_context: UpdateContext

        bot: Bot
        dispatcher: Dispatcher

        facade: BaseUpdateFacade[Any]

        storage: Maybe[Storage]
        state_manager: Maybe[StateManager]
        raw_state: Maybe[str | None]
