from abc import ABC, abstractmethod

from maxo.alta.facades.methods.base import BaseMethodsFacade
from maxo.omit import Omittable, Omitted
from maxo.types.method_results.method import MethodResult
from maxo.types.types.callback import Callback
from maxo.types.types.new_message_body import NewMessageBody


class CallbackMethodsFacade(BaseMethodsFacade, ABC):
    @property
    @abstractmethod
    def callback(self) -> Callback:
        raise NotImplementedError

    async def callback_answer(
        self,
        notification: Omittable[str | None] = Omitted(),
        message: NewMessageBody | None = None,
    ) -> MethodResult:
        return await self.bot.callback_answer(
            callback_id=self.callback.callback_id,
            notification=notification,
            message=message,
        )
