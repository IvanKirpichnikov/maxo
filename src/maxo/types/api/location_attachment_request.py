from decimal import Decimal

from maxo.types.base import MaxoType


class LocationAttachmentRequest(MaxoType):
    """
    Запрос на прикрепление локации.

    Args:
        latitude: Ширина
        longitude: Долгота

    """

    latitude: Decimal
    longitude: Decimal
