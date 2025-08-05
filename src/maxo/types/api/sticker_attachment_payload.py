from maxo.types.base import MaxoType


class StickerAttachmentPayload(MaxoType):
    """
    Содержимое вложения стикера.

    Args:
        url: URL медиа-вложения. Для видео-вложения используйте метод `GetVideoAttachmentDetails`, чтобы получить прямые ссылки.
        code: ID стикера.

    """

    url: str
    code: str
