import logging
import os

from magic_filter import F

from maxo import Bot, Ctx, Dispatcher, SimpleRouter
from maxo.alta.builders import KeyboardBuilder
from maxo.alta.facades import MessageCallbackFacade, MessageCreatedFacade
from maxo.alta.long_polling.long_polling import LongPolling
from maxo.integrations.magic_filter import MagicFilter
from maxo.routing.filters import CommandStart
from maxo.routing.updates import MessageCallback, MessageCreated
from maxo.routing.utils import inline_ctx

router = SimpleRouter()


@router.message_created(CommandStart())
@inline_ctx
async def start_handler(
    update: MessageCreated,
    ctx: Ctx[MessageCreated],
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
@inline_ctx
async def click_me_handler(
    update: MessageCallback,
    ctx: Ctx[MessageCallback],
    facade: MessageCallbackFacade,
) -> None:
    await facade.callback_answer("Ты кликнул на меня")


def main() -> None:
    bot = Bot(os.environ["TOKEN"])
    dispatcher = Dispatcher()
    dispatcher.include(router)

    LongPolling(dispatcher).run(bot)


logging.basicConfig(level=logging.INFO)
main()
