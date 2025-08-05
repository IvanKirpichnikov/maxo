from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType


class SendChatActionResult(MaxoType):
    """
    Результат отправленного действия в чат.

    Args:
        success: `True`, если запрос был успешным, `False` в противном случае.
        message: Объяснительное сообщение, если результат не был успешным.

    """

    success: bool
    message: Omittable[str] = Omitted()
