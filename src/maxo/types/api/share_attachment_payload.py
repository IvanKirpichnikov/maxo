from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType


class ShareAttachmentPayload(MaxoType):
    """
    Полезная нагрузка вложения обмена.

    Args:
        url: URL, прикрепленный к сообщению в качестве предпросмотра медиа. От 1 символа.
        token: Токен вложения.

    """

    url: Omittable[str | None] = Omitted()
    token: Omittable[str | None] = Omitted()
