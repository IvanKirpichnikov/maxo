from retejo.core.markers import Omittable, Omitted
from retejo.http.markers import QueryParam

from maxo.bot.method_results.chats.get_chats import GetChatsResult
from maxo.bot.methods.base import MaxoMethod


class GetChats(MaxoMethod[GetChatsResult]):
    """
    Получение списка всех чатов.

    Возвращает информацию о чатах, в которых участвовал бот.
    Результат включает список чатов и маркер для перехода к следующей странице.

    Источник: https://dev.max.ru/docs-api/methods/GET/chats

    Args:
        count: Количество запрашиваемых чатов. По умолчанию: 50. От 1 до 100.
        marker: Указатель на следующую страницу данных. Для первой страницы передайте null.

    """

    __url__ = "chats"
    __http_method__ = "get"

    count: QueryParam[Omittable[int]] = 50
    marker: QueryParam[Omittable[int | None]] = Omitted()
