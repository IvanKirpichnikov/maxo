from collections.abc import Sequence

from retejo.http.markers import Body, QueryParam

from maxo.bot.method_results.messages.send_message import SendMessageResult
from maxo.bot.methods.base import MaxoMethod
from maxo.omit import Omittable, Omitted
from maxo.types.api.new_message_link import NewMessageLink
from maxo.types.api.request_attachments import AttachmentsRequests
from maxo.types.enums.text_fromat import TextFormat


class SendMessage(MaxoMethod[SendMessageResult]):
    """
    Отправить сообщение.

    Отправляет сообщение в чат.

    Медиафайлы прикрепляются к сообщениям поэтапно:

    1. Получите URL для загрузки медиафайлов.
    2. Загрузите бинарные данные соответствующего формата по полученному URL.
    3. После успешной загрузки получите JSON-объект в ответе.
       Используйте этот объект для создания вложения.

    Источник: https://dev.max.ru/docs-api/methods/POST/messages

    Args:
        user_id: Если вы хотите отправить сообщение пользователю, укажите его ID.
        chat_id: Если сообщение отправляется в чат, укажите его ID.
        disable_link_preview: Если `False`, сервер не будет генерировать превью для ссылок в тексте сообщения.
        text: Новый текст сообщения. До 4000 символов.
        attachments: Новый текст сообщения.
        link: Ссылка на сообщение.
        notify: Если `False`, участники чата не будут уведомлены (по умолчанию true).
        format:
            Если установлен, текст сообщения будет форматрован данным способом.
            Для подробной информации загляните в раздел "Форматирование".

    """

    __url__ = "messages"
    __http_method__ = "post"

    user_id: QueryParam[Omittable[int]] = Omitted()
    chat_id: QueryParam[Omittable[int]] = Omitted()
    disable_link_preview: QueryParam[Omittable[bool]] = Omitted()

    text: Body[str | None] = None
    attachments: Body[Sequence[AttachmentsRequests] | None] = None
    link: Body[NewMessageLink | None] = None
    notify: Body[Omittable[bool]] = True
    format: Body[Omittable[TextFormat | None]] = Omitted()
