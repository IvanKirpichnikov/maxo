from retejo.core.markers import Omittable, Omitted
from retejo.http.markers import Body, UrlVar

from maxo.bot.methods.base import MaxoMethod
from maxo.types.api.chat import Chat
from maxo.types.api.photo_attachment_request_payload import PhotoAttachmentRequestPayload


class EditChat(MaxoMethod[Chat]):
    """
    Изменение информации о чате.

    Позволяет редактировать информацию о чате, включая название, иконку и закреплённое сообщение.

    Источник: https://dev.max.ru/docs-api/methods/PATCH/chats/-chatId-

    Args:
        chat_id: ID чата.
        icon: Запрос на прикрепление изображения (все поля являются взаимоисключающими)
        title: Название. от 1 до 200 символов.
        pin:
            ID сообщения для закрепления в чате.
            Чтобы удалить закреплённое сообщение, используйте метод `unpin`.
        notify: Если `True`, участники получат системное уведомление об изменении.

    """

    __url__ = "chats/{chat_id}"
    __http_method__ = "patch"

    chat_id: UrlVar[int]

    icon: Body[Omittable[PhotoAttachmentRequestPayload | None]] = Omitted()
    title: Body[Omittable[str | None]] = Omitted()
    pin: Body[Omittable[str | None]] = Omitted()
    notify: Body[Omittable[bool | None]] = True
