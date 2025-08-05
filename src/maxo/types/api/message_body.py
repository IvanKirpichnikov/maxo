from maxo.omit import Omittable, Omitted
from maxo.types.api.attachments import Attachments
from maxo.types.api.markup_elements import MarkupElements
from maxo.types.base import MaxoType


class MessageBody(MaxoType):
    """
    Схема, представляющая тело сообщения.

    Args:
        mid: Уникальный ID сообщения
        seq: ID последовательности сообщения в чате
        text: Новый текст сообщения
        attachments: Вложения сообщения. Могут быть одним из типов Attachment. Смотрите описание схемы
        markup: Разметка текста сообщения. Для подробной информации загляните в раздел Форматирование

    """

    mid: str
    seq: int
    text: str | None = None
    attachments: list[Attachments] | None = None
    markup: Omittable[list[MarkupElements] | None] = Omitted()
