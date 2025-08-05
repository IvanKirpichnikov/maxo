import logging
import os

from maxo import Bot, Dispatcher
from maxo.alta.facades.updates.message_created import MessageCreatedFacade
from maxo.alta.long_polling.long_polling import LongPolling
from maxo.routing.ctx import Ctx
from maxo.routing.updates.message_created import MessageCreated
from maxo.routing.utils.inline_ctx import inline_ctx

bot = Bot(os.environ["TOKEN"])
dispatcher = Dispatcher()


@dispatcher.message_created()
@inline_ctx
async def echo_handler(
    update: MessageCreated,
    ctx: Ctx[MessageCreated],
    facade: MessageCreatedFacade,
) -> None:
    text = update.message.unsafe_body.text or "Текста нет"
    await facade.answer_text(text)


logging.basicConfig(level=logging.INFO)
LongPolling(dispatcher).run(bot)
