from datetime import datetime

from retejo.core.markers import Omittable, Omitted
from retejo.http.markers import QueryParam

from maxo.bot.method_results.messages.get_messages import GetMessagesResult
from maxo.bot.methods.base import MaxoMethod


class GetMessages(MaxoMethod[GetMessagesResult]):
    """
    Получение сообщений.

    Возвращает сообщения в чате: страницу с результатами и маркер, указывающий на следующую страницу.
    Сообщения возвращаются в обратном порядке, то есть последние сообщения в чате будут первыми в массиве.
    Поэтому, если вы используете параметры `from_` и `to`, то `to` должно быть меньше, чем `from_`.

    Args:
        chat_id: ID чата, чтобы получить сообщения из определённого чата.
        message_ids: Список ID сообщений, которые нужно получить (через запятую).
        from_: Время начала для запрашиваемых сообщений (в формате Unix timestamp).
        to: Время окончания для запрашиваемых сообщений (в формате Unix timestamp).
        count: Максимальное количество сообщений в ответе. По умолчанию: 50.

    """

    __url__ = "messages"
    __http_method__ = "get"

    chat_id: QueryParam[Omittable[int]] = Omitted()
    message_ids: QueryParam[Omittable[list[int] | None]] = Omitted()
    from_: QueryParam[Omittable[datetime]] = Omitted()
    to: QueryParam[Omittable[datetime]] = Omitted()
    count: QueryParam[Omittable[int]] = 50
