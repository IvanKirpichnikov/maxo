from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Final, Protocol

DESTINY_DEFAULT: Final = "default"


@dataclass(frozen=True, slots=True)
class StorageKey:
    bot_id: int
    chat_id: int | None = None
    user_id: int | None = None
    destiny: str = DESTINY_DEFAULT


class StorageKeyType(str, Enum):
    DATA = "data"
    STATE = "state"
    LOCK = "lock"


class KeyBuilder(Protocol):
    __slots__ = ()

    @abstractmethod
    def build(
        self,
        key: StorageKey,
        type_: StorageKeyType | None = None,
    ) -> str:
        raise NotImplementedError


class DefaultKeyBuilder(KeyBuilder):
    __slots__ = (
        "prefix",
        "separator",
        "with_bot_id",
        "with_destiny",
    )

    def __init__(
        self,
        *,
        prefix: str = "fsm",
        separator: str = ":",
        with_bot_id: bool = False,
        with_destiny: bool = False,
    ) -> None:
        self.prefix = prefix
        self.separator = separator
        self.with_bot_id = with_bot_id
        self.with_destiny = with_destiny

    def build(
        self,
        key: StorageKey,
        type_: StorageKeyType | None = None,
    ) -> str:
        parts = [self.prefix, str(key.chat_id), str(key.user_id)]

        if self.with_bot_id:
            parts.append(str(key.bot_id))

        if self.with_destiny:
            parts.append(key.destiny)
        elif key.destiny != DESTINY_DEFAULT:
            raise ValueError(f"Use `with_destiny=True` in for {self.__class__.__name__}")

        if type_:
            parts.append(type_.value)

        return self.separator.join(parts)
