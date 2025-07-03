import logging
import os

from magic_filter import F

from maxo.bot import Bot
from maxo.builders import KeyboardBuilder
from maxo.dispatcher import Dispatcher, Router
from maxo.facades import MessageCallbackFacade, MessageCreatedFacade
from maxo.filters.command import CommandStart
from maxo.filters.magic_filter import MagicFilter
from maxo.types import MessageCreated, MessageCallback

router = Router(__name__)


@router.message_created(CommandStart())
async def start_handler(
    update: MessageCreated,
    facade: MessageCreatedFacade,
) -> None:
    keyboard = (
        KeyboardBuilder()
        .add_callback(
            text="Кликни на меня",
            payload="click_me",
        )
        .add_chat(
            text="Создать чат",
            title="Чат",
        )
        .add_link(text="Ссылка на google", url="https://google.com")
        .add_request_contact(text="Поделится контактами")
        .add_request_geo_location(text="Поделится гео позицией")
        .adjust(3)
    )

    await facade.answer_text(
        "Клавиатура",
        keyboard=keyboard.build(),
    )


@router.message_callback(MagicFilter(F.callback_id == "click_me"))
async def click_me_handler(
    update: MessageCallback,
    facade: MessageCallbackFacade,
) -> None:
    await facade.callback_answer("Ты кликнул на меня")


def main() -> None:
    TOKEN = os.environ["TOKEN"]

    bot = Bot(TOKEN)
    dispatcher = Dispatcher()
    dispatcher.include(router)

    dispatcher.run_polling(bot)


logging.basicConfig(level=logging.INFO)
main()
