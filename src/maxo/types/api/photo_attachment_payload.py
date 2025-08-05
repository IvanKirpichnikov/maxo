from maxo.types.base import MaxoType


class PhotoAttachmentPayload(MaxoType):
    """
    Содержимое вложения фотографии.

    Args:
        photo_id: Уникальный ID этого изображения
        token: Используйте token, если вы пытаетесь повторно использовать одно и то же вложение в другом сообщении.
        url: URL изображения

    """

    photo_id: int
    token: str
    url: str
