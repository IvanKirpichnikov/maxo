from abc import abstractmethod
from typing import Protocol

from maxo.bot.api_client import MaxApiClient
from maxo.errors.state import EmptyStateError
from maxo.types.bot.me import Me


class BotState(Protocol):
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
        raise EmptyStateError

    @property
    def started(self) -> bool:
        return False

    @property
    def closed(self) -> bool:
        return False

    @property
    def me(self) -> Me:
        raise EmptyStateError


class ClosedBotState(BotState):
    @property
    def api_client(self) -> MaxApiClient:
        raise EmptyStateError

    @property
    def started(self) -> bool:
        return False

    @property
    def closed(self) -> bool:
        return True

    @property
    def me(self) -> Me:
        raise EmptyStateError


class InitialBotState(BotState):
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
