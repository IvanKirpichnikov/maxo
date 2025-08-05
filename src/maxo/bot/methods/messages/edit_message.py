from collections.abc import Sequence

from retejo.http.markers import Body, QueryParam

from maxo.bot.method_results.messages.edit_message import EditMessageResult
from maxo.bot.methods.base import MaxoMethod
from maxo.omit import Omittable, Omitted
from maxo.types.api.new_message_link import NewMessageLink
from maxo.types.api.request_attachments import AttachmentsRequests
from maxo.types.enums.text_fromat import TextFormat


class EditMessage(MaxoMethod[EditMessageResult]):
    """
    Редактировать сообщение.

    Редактирует сообщение в чате. Если поле attachments равно null,
    вложения текущего сообщения не изменяются.
    Если в этом поле передан пустой список, все вложения будут удалены.

    Источник: https://dev.max.ru/docs-api/methods/PUT/messages

    Args:
        message_id: ID редактируемого сообщения. От 1 символа.
        text: Новый текст сообщения. До 4000 символов.
        attachments: Вложения сообщения. Если пусто, все вложения будут удалены.
        link: Ссылка на сообщение.
        notify: Если `False`, участники чата не будут уведомлены.
        format:
            Если установлен, текст сообщения будет форматрован данным способом.
            Для подробной информации загляните в раздел "Форматирование"

    """

    __url__ = "messages"
    __http_method__ = "put"

    message_id: QueryParam[str]

    text: Body[str | None] = None
    attachments: Body[Sequence[AttachmentsRequests] | None] = None
    link: Body[NewMessageLink | None] = None
    notify: Body[Omittable[bool]] = True
    format: Body[Omittable[TextFormat | None]] = Omitted()
