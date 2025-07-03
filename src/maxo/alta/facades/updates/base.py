from typing import Generic, TypeVar

from maxo.kerno.bot.bot import Bot
from maxo.kerno.types.updates.base import BaseUpdate

U = TypeVar("U", bound=BaseUpdate)


class BaseUpdateFacade(Generic[U]):
    def __init__(
        self,
        bot: Bot,
        update: U,
    ) -> None:
        self._bot = bot
        self._update = update

    @property
    def bot(self) -> Bot:
        return self._bot
