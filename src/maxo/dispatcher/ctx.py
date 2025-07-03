from collections.abc import MutableMapping
from typing import TYPE_CHECKING, Any, Generic, TypeAlias, TypeVar, cast

from maxo.bot.bot import Bot
from maxo.state.manager import StateManager
from maxo.state.storages.base import Storage
from maxo.types.update_context import UpdateContext
from maxo.types.updates.base import BaseUpdate

if TYPE_CHECKING:
    from maxo.dispatcher.dispatcher import Dispatcher

CtxData: TypeAlias = MutableMapping[str, Any]

U = TypeVar("U", bound=BaseUpdate)


class Ctx(Generic[U]):
    def __init__(
        self,
        update: U,
        data: CtxData,
    ) -> None:
        self._update = update
        self._data = data

        self["update_event"] = update

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.data[key] = value

    def __delitem__(self, key: str) -> None:
        del self.data[key]

    def get(self, key: str, default: Any = None) -> Any | None:
        return self._data.get(key, default)

    @property
    def data(self) -> CtxData:
        return self._data

    @property
    def update(self) -> U:
        return self._update

    @property
    def update_tp(self) -> type[U]:
        return type(self._update)

    @property
    def update_context(self) -> UpdateContext:
        return cast("UpdateContext", self["update_context"])

    @property
    def bot(self) -> Bot:
        return cast("Bot", self["bot"])

    @property
    def dispatcher(self) -> "Dispatcher":
        return cast("Dispatcher", self["dispatcher"])

    @property
    def storage(self) -> Storage:
        return cast("Storage", self["storage"])

    @property
    def state_manager(self) -> StateManager:
        return cast("StateManager", self["state_manager"])

    @property
    def raw_state(self) -> str | None:
        return cast("str | None", self["raw_state"])
