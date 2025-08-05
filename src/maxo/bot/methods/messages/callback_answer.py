from retejo.http.markers import Body, QueryParam

from maxo.bot.method_results.messages.callback_answer import CallbackAnswerResult
from maxo.bot.methods.base import MaxoMethod
from maxo.omit import Omittable, Omitted
from maxo.types.api.new_message_body import NewMessageBody


class CallbackAnswer(MaxoMethod[CallbackAnswerResult]):
    """
    Ответ на callback.

    Этот метод используется для отправки ответа после того,
    как пользователь нажал на кнопку. Ответом может быть
    обновленное сообщение и/или одноразовое уведомление для пользователя.

    Источник: https://dev.max.ru/docs-api/methods/POST/answers

    Args:
        callback_id:
            Идентификатор кнопки, по которой пользователь кликнул.
            Бот получает идентификатор как часть `Update` с типом `message_callback`.
            Можно получить из `GET:/updates` через поле `updates[i].callback.callback_id`.
            От 1 символа.
        message: Заполните это, если хотите изменить текущее сообщение.
        notification: Заполните это, если хотите просто отправить одноразовое уведомление пользователю.

    """

    __url__ = "answers"
    __http_method__ = "post"

    callback_id: QueryParam[str]

    message: Body[NewMessageBody | None] = None
    notification: Body[Omittable[str | None]] = Omitted()
