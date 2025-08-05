import logging
import os

from magic_filter import F

from maxo import Bot, Dispatcher, SimpleRouter
from maxo.alta.facades import MessageCreatedFacade
from maxo.alta.long_polling.long_polling import LongPolling
from maxo.alta.state_system import State, StateFilter, StateManager, StatesGroup
from maxo.integrations.magic_filter import MagicFilter
from maxo.routing.ctx import Ctx
from maxo.routing.filters import CommandStart
from maxo.routing.updates.message_created import MessageCreated
from maxo.routing.utils import inline_ctx
from maxo.types.enums import TextFormat

router = SimpleRouter(__name__)


class UserRegistatorStatesGroup(StatesGroup):
    INPUT_NAME = State()
    INPUT_AGE = State()


@router.message_created(CommandStart())
@inline_ctx
async def start_handler(
    update: MessageCreated,
    ctx: Ctx[MessageCreated],
    facade: MessageCreatedFacade,
    state_manager: StateManager,
) -> None:
    await facade.reply_text("Привет. Заполни анкету.")
    await facade.answer_text("Введи имя.")
    await state_manager.set_state(UserRegistatorStatesGroup.INPUT_NAME)


@router.message_created(MagicFilter(F.message.body.text) & StateFilter(UserRegistatorStatesGroup.INPUT_NAME))
@inline_ctx
async def input_name_handler(
    update: MessageCreated,
    ctx: Ctx[MessageCreated],
    facade: MessageCreatedFacade,
    state_manager: StateManager,
) -> None:
    await facade.delete_message()

    text = update.message.unsafe_body.text
    if text is None:
        await facade.answer_text("Отправь текстовое сообщение")
        return None

    await facade.reply_text("Теперь отправь возраст")
    await facade.answer_text(
        f"Анкета:\n<b>Имя</b>: {text}\n<b>Возраст</b>: отсутствует\n",
        format=TextFormat.HTML,
    )

    await state_manager.update_data(name=text)
    await state_manager.set_state(UserRegistatorStatesGroup.INPUT_AGE)


@router.message_created(MagicFilter(F.message.body.text) & StateFilter(UserRegistatorStatesGroup.INPUT_AGE))
@inline_ctx
async def input_age_handler(
    update: MessageCreated,
    ctx: Ctx[MessageCreated],
    facade: MessageCreatedFacade,
    state_manager: StateManager,
) -> None:
    await facade.delete_message()

    text = update.message.unsafe_body.text
    if text is None:
        await facade.answer_text("Отправь текстовое сообщение")
        return None

    try:
        age = int(text)
    except TypeError:
        await facade.answer_text("Ты отправил не возраст. Попробуй еще раз")
        return None

    name = await state_manager.get_value("name")

    await facade.answer_text("Ты успешно заполнил анкету")
    await facade.answer_text(
        f"Анкета:\n<b>Имя</b>: {name}\n<b>Возраст</b>: {age}\n",
        format=TextFormat.HTML,
    )

    await state_manager.clear()


def main() -> None:
    bot = Bot(os.environ["TOKEN"])
    dispatcher = Dispatcher()

    dispatcher.include(router)

    LongPolling(dispatcher).run(bot)


logging.basicConfig(level=logging.INFO)
main()
