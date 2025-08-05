from maxo.types.base import MaxoType


class StickerAttachmentRequestPayload(MaxoType):
    """
    Данные запроса на прикрепление стикера.

    Args:
        code: Код стикера

    """

    code: str
