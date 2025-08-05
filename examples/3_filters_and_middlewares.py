import logging
import os
from typing import Any

from maxo import Bot, Ctx, Dispatcher
from maxo.alta.facades import MessageCreatedFacade
from maxo.alta.long_polling.long_polling import LongPolling
from maxo.routing.filters.base import BaseFilter
from maxo.routing.interfaces.middleware import Middleware, NextMiddleware
from maxo.routing.updates.message_created import MessageCreated
from maxo.routing.utils.inline_ctx import inline_ctx


class OuterMiddleware(Middleware[MessageCreated]):
    async def execute(
        self,
        update: MessageCreated,
        ctx: Ctx[MessageCreated],
        next: NextMiddleware[MessageCreated],
    ) -> Any:
        print("Исполнится перед фильтрами")  # noqa: T201
        result = await next(ctx)
        print("Исполнится после фильтров")  # noqa: T201
        return result


class InnerMiddleware(Middleware[MessageCreated]):
    async def execute(
        self,
        update: MessageCreated,
        ctx: Ctx[MessageCreated],
        next: NextMiddleware[MessageCreated],
    ) -> Any:
        print("Исполнится перед хендлером")  # noqa: T201
        result = await next(ctx)
        print("Исполнится после хендлера")  # noqa: T201
        return result


class ContainsTextFilter(BaseFilter[MessageCreated]):
    def __init__(self, text: str) -> None:
        self._text = text

    async def execute(
        self,
        update: MessageCreated,
        ctx: Ctx[MessageCreated],
    ) -> bool:
        if update.message.body is None:
            return False
        if update.message.body.text is None:
            return False

        return self._text in update.message.body.text


dispatcher = Dispatcher()
dispatcher.message_created.middleware.inner(InnerMiddleware())
dispatcher.message_created.middleware.outer(InnerMiddleware())


@dispatcher.message_created((ContainsTextFilter("gojo") & ContainsTextFilter("maki")) | ContainsTextFilter("sukuna"))
@inline_ctx
async def echo_handler(
    update: MessageCreated,
    ctx: Ctx[MessageCreated],
    facade: MessageCreatedFacade,
) -> None:
    print("Исполнение хендлера")  # noqa: T201


logging.basicConfig(level=logging.INFO)
bot = Bot(os.environ["TOKEN"])
LongPolling(dispatcher).run(bot)
