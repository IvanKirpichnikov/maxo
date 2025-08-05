from maxo.omit import Omittable, Omitted
from maxo.types.api.user import User
from maxo.types.base import MaxoType


class ContactAttachmentPayload(MaxoType):
    """
    Содержимое вложения контактов.

    Args:
        vcf_info: Информация о пользователе в формате VCF.
        max_info: Информация о пользователе

    """

    vcf_info: Omittable[str | None] = Omitted()
    max_info: Omittable[User | None] = Omitted()
