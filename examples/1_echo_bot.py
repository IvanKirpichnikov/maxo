import os

from maxo.bot import Bot
from maxo.dispatcher import Dispatcher
from maxo.facades import MessageCreatedFacade
from maxo.types import MessageCreated

TOKEN = os.environ["TOKEN"]

bot = Bot(TOKEN)
dispatcher = Dispatcher()


@dispatcher.message_created()
async def echo_handler(
    update: MessageCreated,
    facade: MessageCreatedFacade,
) -> None:
    text = update.message.unsafe_body.text
    await facade.answer_text(text or "Текста нет")


dispatcher.run_polling(bot)
