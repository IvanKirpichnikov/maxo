import logging
import os
from magic_filter import F

from maxo import Bot, Dispatcher, Router
from maxo.enums import TextFormat
from maxo.facades import MessageCreatedFacade
from maxo.filters import CommandStart, MagicFilter, StateFilter
from maxo.state import StateManager, State, StatesGroup
from maxo.types import MessageCreated

router = Router(__name__)

class UserRegistatorStatesGroup(StatesGroup):
    INPUT_NAME = State()
    INPUT_AGE = State()


@router.message_created(CommandStart())
async def start_handler(
    update: MessageCreated,
    facade: MessageCreatedFacade,
    state_manager: StateManager,
) -> None:
    await facade.reply_text("Привет. Заполни анкету.")
    await facade.answer_text("Введи имя.")
    await state_manager.set_state(UserRegistatorStatesGroup.INPUT_NAME)


@router.message_created(
    MagicFilter(F.message.body.text)
    & StateFilter(UserRegistatorStatesGroup.INPUT_NAME)
)
async def input_name_handler(
    update: MessageCreated,
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
        "Анкета:\n"
        f"<b>Имя</b>: {text}\n"
        f"<b>Возраст</b>: отсутствует\n",
        format=TextFormat.HTML,
    )

    await state_manager.update_data(name=text)
    await state_manager.set_state(UserRegistatorStatesGroup.INPUT_AGE)


@router.message_created(
    MagicFilter(F.message.body.text)
    & StateFilter(UserRegistatorStatesGroup.INPUT_AGE)
)
async def input_age_handler(
    update: MessageCreated,
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
        "Анкета:\n"
        f"<b>Имя</b>: {name}\n"
        f"<b>Возраст</b>: {age}\n",
        format=TextFormat.HTML,
    )

    await state_manager.clear()


def main() -> None:
    TOKEN = os.environ["TOKEN"]

    bot = Bot(TOKEN, warming_up=True)
    dispatcher = Dispatcher()
    dispatcher.include(router)

    dispatcher.run_polling(bot)


logging.basicConfig(level=logging.INFO)
main()
