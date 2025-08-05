from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType


class UploadedInfo(MaxoType):
    """
    Загруженная информация.

    Args:
        token: Токен — уникальный ID загруженного медиафайла.

    """

    token: Omittable[str] = Omitted()
