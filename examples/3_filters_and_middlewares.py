import logging
import os
from typing import Any

from maxo import Bot, Ctx, Dispatcher
from maxo.facades import MessageCreatedFacade
from maxo.filters import Filter
from maxo.middlewares import Middleware, NextMiddleware
from maxo.types import MessageCreated

bot = Bot(os.environ["TOKEN"])
dispatcher = Dispatcher()


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


class ContainsTextFilter(Filter[MessageCreated]):
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


dispatcher.message_created.inner_middleware(InnerMiddleware())
dispatcher.message_created.outer_middleware(InnerMiddleware())


@dispatcher.message_created((ContainsTextFilter("gojo") & ContainsTextFilter("maki")) | ContainsTextFilter("sukuna"))
async def echo_handler(
    update: MessageCreated,
    facade: MessageCreatedFacade,
) -> None:
    print("Исполнение хендлера")  # noqa: T201


logging.basicConfig(level=logging.INFO)
dispatcher.run_polling(bot)
