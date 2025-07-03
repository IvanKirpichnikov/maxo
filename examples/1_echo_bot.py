import logging
import os

from maxo import Bot, Dispatcher
from maxo.facades import MessageCreatedFacade
from maxo.types import MessageCreated

bot = Bot(os.environ["TOKEN"])
dispatcher = Dispatcher()


@dispatcher.message_created()
async def echo_handler(
    update: MessageCreated,
    facade: MessageCreatedFacade,
) -> None:
    text = update.message.unsafe_body.text
    await facade.answer_text(text or "Текста нет")


logging.basicConfig(level=logging.INFO)
dispatcher.run_polling(bot)
