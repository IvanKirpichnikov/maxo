from maxo.types.base import MaxoType
from maxo.types.enums.attachment_type import AttachmentType


class LocationAttachment(MaxoType):
    """
    Вложение локации.

    Args:
        latitude: Широта
        longitude: Долгота

    """

    type = AttachmentType.LOCATION

    latitude: float
    longitude: float
