from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType


class GetDownloadLinkResult(MaxoType):
    """
    Результат получения URL для загрузки файла.

    Args:
        url: URL для загрузки файла.
        token: Видео или аудио-токен для отправки сообщения.

    """

    url: str
    token: Omittable[str] = Omitted()
