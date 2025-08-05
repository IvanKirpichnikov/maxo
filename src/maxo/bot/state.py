from abc import abstractmethod
from typing import Protocol

from maxo.bot.api_client import MaxApiClient
from maxo.errors.state import StateError
from maxo.types.api.bot_info import BotInfo


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
    def info(self) -> BotInfo:
        raise NotImplementedError


class EmptyBotState(BotState):
    @property
    def api_client(self) -> MaxApiClient:
        raise StateError("Not started bot")

    @property
    def started(self) -> bool:
        return False

    @property
    def closed(self) -> bool:
        return False

    @property
    def info(self) -> BotInfo:
        raise StateError("Not started bot")


class ClosedBotState(BotState):
    @property
    def api_client(self) -> MaxApiClient:
        raise StateError("Bot closed")

    @property
    def started(self) -> bool:
        return False

    @property
    def closed(self) -> bool:
        return True

    @property
    def info(self) -> BotInfo:
        raise StateError("Bot closed")


class InitialBotState(BotState):
    __slots__ = ("_api_client", "_info")

    def __init__(
        self,
        info: BotInfo,
        api_client: MaxApiClient,
    ) -> None:
        self._info = info
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
    def info(self) -> BotInfo:
        return self._info
