from abc import ABC, abstractmethod

from maxo.kerno.bot.bot import Bot


class BaseMethodsFacade(ABC):
    @property
    @abstractmethod
    def bot(self) -> Bot:
        raise NotImplementedError
