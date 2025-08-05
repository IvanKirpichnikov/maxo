from collections.abc import Sequence

from retejo.core.markers import Omittable, Omitted
from retejo.http.markers import QueryParam

from maxo.bot.method_results.subscriptions.get_updates import GetUpdatesResult
from maxo.bot.methods.base import MaxoMethod


class GetUpdates(MaxoMethod[GetUpdatesResult]):
    """
    Получение обновлений.

    Этот метод можно использовать для получения обновлений,
    если ваш бот не подписан на WebHook.
    Метод использует долгий опрос (long polling).

    Каждое обновление имеет свой номер последовательности.
    Свойство marker в ответе указывает на следующее ожидаемое обновление.

    Все предыдущие обновления считаются завершенными после прохождения параметра marker.
    Если параметр marker не передан, бот получит все обновления, произошедшие после последнего подтверждения.

    Args:
        limit:
            Максимальное количество обновлений для получения.
            По умолчанию 100. От 1 до 1000 включительно.
        timeout:
            Тайм-аут в секундах для долгого опроса.
            По умолчанию 30. от 0 до 90 включительно.
        marker:
            Если передан, бот получит обновления, которые еще не были получены.
            Если не передан, получит все новые обновления.
        types: Список типов обновлений, которые бот хочет получить.

    """

    __url__ = "updates"
    __http_method__ = "get"

    limit: QueryParam[Omittable[int]] = 100
    timeout: QueryParam[Omittable[int]] = 30
    marker: QueryParam[Omittable[int | None]] = Omitted()
    types: QueryParam[Omittable[Sequence[str]]] = Omitted()
