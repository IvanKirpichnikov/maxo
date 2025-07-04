from abc import abstractmethod
from typing import Protocol

from maxo.errors.state import StateError
from maxo.kerno.bot.api_client import MaxApiClient
from maxo.kerno.types.types.me import Me


class BotState(Protocol):
    __slots__ = ()

    @property
    @abstractmethod
    def api_client(self) -> MaxApiClient:
        raise NotImplementedError

    @property
    @abstractmethod
    def started(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def closed(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def me(self) -> Me:
        raise NotImplementedError


class EmptyBotState(BotState):
    @property
    def api_client(self) -> MaxApiClient:
        raise StateError

    @property
    def started(self) -> bool:
        return False

    @property
    def closed(self) -> bool:
        return False

    @property
    def me(self) -> Me:
        raise StateError


class ClosedBotState(BotState):
    @property
    def api_client(self) -> MaxApiClient:
        raise StateError

    @property
    def started(self) -> bool:
        return False

    @property
    def closed(self) -> bool:
        return True

    @property
    def me(self) -> Me:
        raise StateError


class InitialBotState(BotState):
    __slots__ = ("_api_client", "_me")

    def __init__(
        self,
        me: Me,
        api_client: MaxApiClient,
    ) -> None:
        self._me = me
        self._api_client = api_client

    @property
    def api_client(self) -> MaxApiClient:
        return self._api_client

    @property
    def started(self) -> bool:
        return True

    @property
    def closed(self) -> bool:
        return False

    @property
    def me(self) -> Me:
        return self._me
