from maxo.omit import Omittable, Omitted
from maxo.types.api.user import User


class UserWithPhoto(User):
    """
    Информация о пользователе c фото.

    Args:
        avatar_url: URL аватара
        full_avatar_url: URL аватара большего размера

    """

    avatar_url: Omittable[str] = Omitted()
    full_avatar_url: Omittable[str] = Omitted()
