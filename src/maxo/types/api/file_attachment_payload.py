from maxo.types.base import MaxoType


class FileAttachmentPayload(MaxoType):
    """
    Содержимое файлового вложения.

    Args:
        url: URL медиа-вложения. Для видео-вложения используйте метод `GetVideoAttachmentDetails`, чтобы получить прямые ссылки.
        token: Используйте token, если вы пытаетесь повторно использовать одно и то же вложение в другом сообщении.

    """

    url: str
    token: str
