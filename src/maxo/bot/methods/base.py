from typing import Generic, TypeVar

from retejo.http.entities import HttpMethod
from retejo.http.markers import QueryParam

from maxo.omit import Omittable, Omitted

_MethodResultT = TypeVar("_MethodResultT")


class MaxoMethod(HttpMethod[_MethodResultT], Generic[_MethodResultT]):
    """
    Базовый метод для методов Bot API Max.

    Args:
        access_token: Токен бота. По умолчанию используется переданный токен в Bot.

    """

    access_token: QueryParam[Omittable[str]] = Omitted()
